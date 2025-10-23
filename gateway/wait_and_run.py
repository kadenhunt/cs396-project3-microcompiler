import time
import requests
import sys
import subprocess

LEXER = 'http://lexer:5001/healthz'
PARSER = 'http://parser:5002/healthz'
CODEGEN = 'http://codegen:5003/healthz'

ENDPOINTS = [LEXER, PARSER, CODEGEN]

MAX_RETRIES = 20
SLEEP = 1


def wait_for_services():
    for endpoint in ENDPOINTS:
        ok = False
        for i in range(MAX_RETRIES):
            try:
                r = requests.get(endpoint, timeout=1)
                if r.status_code == 200:
                    print(f"{endpoint} is healthy")
                    ok = True
                    break
            except Exception as e:
                pass
            print(f"waiting for {endpoint} ({i+1}/{MAX_RETRIES})")
            time.sleep(SLEEP)
        if not ok:
            print(f"Service {endpoint} failed to become healthy")
            return False
    return True


if __name__ == '__main__':
    if not wait_for_services():
        print('One or more services not healthy, exiting')
        sys.exit(1)

    # start uvicorn normally
    subprocess.run(["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "5000"])