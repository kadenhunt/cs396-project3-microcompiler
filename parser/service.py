from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, List, Optional
from core_parser import Parser

app = FastAPI(title="parser")

class Token(BaseModel):
    type: str
    value: Optional[Any] = None

class InTokens(BaseModel):
    tokens: List[Token]

@app.post("/parse")
def parse(body: InTokens):
    try:
        toks = [(t.type, t.value) if t.value is not None else (t.type,) for t in body.tokens]
        ast = Parser(toks).parse_program()
        def ser(node):
            if isinstance(node, tuple): return list(node)
            if isinstance(node, list): return [ser(n) for n in node]
            return node
        return {"ast": ser(ast)}
    except Exception as e:
        return {"error": {"phase": "parser", "message": str(e)}}


@app.get("/healthz")
def healthz():
    return {"ok": True, "phase": "parser"}
