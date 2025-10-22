from fastapi import FastAPI
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
def compile_code(body: Source):
    # 1) tokenize
    t = requests.post(f"{LEXER_URL}/tokenize", json={"source": body.source})
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

    # Return machine code and a download link (proxied from codegen)
    return {
        "machine": gj.get("machine", ""),
        "download": f"{CODEGEN_URL}/download"  # exposed on localhost via compose
    }
