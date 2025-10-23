from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
import requests

# Use container DNS names set by Compose: lexer, parser, codegen
LEXER_URL = "http://lexer:5001"
PARSER_URL = "http://parser:5002"
CODEGEN_URL = "http://codegen:5003"

app = FastAPI(title="gateway", version="1.0.0")

class Source(BaseModel):
    source: str

@app.get("/")
def index():
    return {"service": "gateway", "endpoints": ["POST /compile"]}

@app.get("/healthz")
def healthz():
    return {"ok": True, "phase": "gateway"}

@app.post("/compile")
async def compile_code(request: Request):
    # Accept either properly-formed JSON {"source":"..."}
    # or PowerShell-style objects where source is an object with a `value` field
    # or raw text body. Coerce to a plain Python string before forwarding.
    try:
        payload = await request.json()
    except Exception:
        payload = None

    src = None
    if isinstance(payload, dict) and 'source' in payload:
        src = payload['source']
        # PowerShell sometimes wraps values into an object with a 'value' key
        if isinstance(src, dict) and 'value' in src:
            src = src['value']
        # If it's not a string, coerce to string
        if not isinstance(src, str):
            src = str(src)
    else:
        # fallback: read raw body
        body_bytes = await request.body()
        try:
            src = body_bytes.decode('utf-8')
        except Exception:
            src = str(body_bytes)

    # If we still don't have a source, return a validation-like error
    if src is None:
        return {"error": {"phase": "gateway", "message": "missing source in request"}}

    # 1) tokenize
    t = requests.post(f"{LEXER_URL}/tokenize", json={"source": src})
    tj = t.json()
    if "error" in tj:
        return {"error": {"phase": "lexer", **tj["error"]}}

    # 2) parse
    p = requests.post(f"{PARSER_URL}/parse", json={"tokens": tj["tokens"]})
    pj = p.json()
    if "error" in pj:
        return {"error": {"phase": "parser", **pj["error"]}}

    # 3) generate
    g = requests.post(f"{CODEGEN_URL}/generate", json={"ast": pj["ast"]})
    gj = g.json()
    if "error" in gj:
        return {"error": {"phase": "codegen", **gj["error"]}}

    # Return machine code and a download link (proxied through the gateway)
    download_url = str(request.base_url) + "download"
    return {
        "machine": gj.get("machine", ""),
        "download": download_url
    }


@app.get("/download")
def download_proxy():
    # Proxy the download through the gateway so clients can fetch from localhost:5000/download
    r = requests.get(f"{CODEGEN_URL}/download", stream=True)
    return Response(content=r.content, media_type="text/plain")
