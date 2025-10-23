Kaden Hunt and Nate Barner — CS396 Project 3

Microservice three-pass compiler

Abstract
--------
This project implements a minimal three-pass compiler (lexical analysis, parsing, and code generation) where each pass runs as an independent microservice inside a Docker container. The services communicate over HTTP (TCP) and are orchestrated by a gateway which exposes a single `/compile` endpoint. The code generator emits assembly-like instructions and writes the final output to `output/out.asm`.

Prerequisites
-------------
- Docker and Docker Compose installed on the host machine
- Python 3.10+ (for running helper scripts locally)
- PowerShell (Windows) for the provided convenience client scripts; a cross-platform client can be added on request

Two-step run
-----------------------------------------------------
Make sure you run them from the repository root.

```powershell
docker compose up --build -d
.\compile.ps1
```

Note: `compile.ps1` posts the contents of `source.txt` to the gateway. The containers must be running (first command) for the request to succeed. For a one-command demo that waits for readiness and measures elapsed time, use `run_demo.ps1`.

Files of interest
-----------------
- `docker-compose.yml` — Compose configuration that builds and runs the four services (lexer, parser, codegen, gateway).
- `lexer/`, `parser/`, `codegen/`, `gateway/` — per-service directories containing a FastAPI wrapper (`service.py`) and a `Dockerfile`.
- `core_lexer.py`, `core_parser.py`, `core_codegen.py` — the core compiler logic used by the service wrappers.
- `compile.ps1` — PowerShell client that POSTs `source.txt` to the gateway and prints the returned assembly-like text.
- `run_demo.ps1` — convenience wrapper that builds, waits for the gateway, runs `compile.ps1`, measures time, and downloads `output/out.asm`.
- `make_source.py` — helper that generates a ~500-line `source.txt` for performance testing.
- `output/` — host-mounted folder where `out.asm` is written by the codegen service.

How the system works (end-to-end)
---------------------------------
1. The client (e.g., `compile.ps1`) POSTs JSON `{ "source": "..." }` to the gateway at `POST /compile`.
2. The gateway forwards the source to the lexer microservice (`POST /tokenize`) and receives a token list.
3. Tokens are forwarded to the parser microservice (`POST /parse`) which returns a serialized AST.
4. The AST is forwarded to the codegen microservice (`POST /generate`) which emits assembly-like text and writes `/output/out.asm`.
5. The gateway returns JSON containing the `machine` text and provides `GET /download` to fetch the file via HTTP.

API endpoints summary
-----------------------
- Gateway (port 5000)
	- POST /compile — accepts `{ "source": string }`, orchestrates the three passes, returns `machine` and `download` information
	- GET /download — proxies the generated `out.asm` for host download

- Lexer (port 5001)
	- POST /tokenize — accepts source string, returns token list
	- GET /healthz — simple readiness check

- Parser (port 5002)
	- POST /parse — accepts tokens, returns AST
	- GET /healthz — readiness check

- Codegen (port 5003)
	- POST /generate — accepts AST, writes `/output/out.asm`, returns assembly text
	- GET /download — returns `out.asm`
	- GET /healthz — readiness check


Testing and verification
------------------------
- Local check: `python main.py` runs the three passes in-process and writes `out.asm`.
- Containerized check: run the two-step commands above and confirm `output/out.asm` is produced. Use `docker compose logs <service>` to inspect logs for each service.
- Performance test: use `python .\make_source.py` to generate a ~500-line `source.txt` and measure the `run_demo.ps1` compile time (demonstrate the <5s requirement).

GO TOPS!