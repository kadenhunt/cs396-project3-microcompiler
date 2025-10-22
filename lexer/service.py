from fastapi import FastAPI
from pydantic import BaseModel
import tempfile
from lexer import Lexer

app = FastAPI(title="lexer")

class Source(BaseModel):
    source: str

@app.post("/tokenize")
def tokenize(body: Source):
    try:
        with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
            tmp.write(body.source); tmp.flush()
            toks = Lexer(tmp.name).tokens()
        out = []
        for t in toks:
            out.append({"type": t[0], "value": t[1] if len(t) > 1 else None})
        return {"tokens": out}
    except Exception as e:
        return {"error": {"phase": "lexer", "message": str(e)}}
