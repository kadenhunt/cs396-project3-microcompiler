from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Any
import os
from core_codegen import CodeGen

app = FastAPI(title="codegen")

class InAST(BaseModel):
    ast: Any

@app.post("/generate")
def generate(body: InAST):
    try:
        cg = CodeGen()
        cg.generate_program(body.ast, "/output/out.asm")
        with open("/output/out.asm", "r") as f:
            machine = f.read()
        return {"machine": machine, "file": "/output/out.asm"}
    except Exception as e:
        return {"error": {"phase": "codegen", "message": str(e)}}

@app.get("/download")
def download():
    path = "/output/out.asm"
    return FileResponse(path, media_type="text/plain", filename="out.asm")


@app.get("/healthz")
def healthz():
    return {"ok": True, "phase": "codegen"}