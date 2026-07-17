from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "http://127.0.0.1:8123"


def request_json(path: str, payload: dict[str, str] | None = None) -> dict[str, object]:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        headers={"Content-Type": "application/json"} if body else {},
        method="POST" if body else "GET",
    )
    with urllib.request.urlopen(request, timeout=3) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_until_ready() -> dict[str, object]:
    last_error: Exception | None = None
    for _ in range(30):
        try:
            return request_json("/health")
        except (OSError, urllib.error.URLError) as error:
            last_error = error
            time.sleep(0.2)
    raise RuntimeError("API did not become ready") from last_error


def main() -> None:
    creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--app-dir",
            "src",
            "--host",
            "127.0.0.1",
            "--port",
            "8123",
        ],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creation_flags,
    )
    try:
        health = wait_until_ready()
        answer = request_json("/ask", {"question": "Where is the registrar's office?"})
        assert health == {"status": "ok", "provider": "stub"}
        assert answer == {
            "answer": "Stub response for: Where is the registrar's office?",
            "sources": [],
            "confidence": "stub",
            "escalation_flag": False,
        }
        print(json.dumps({"health": health, "ask": answer}, indent=2))
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


if __name__ == "__main__":
    main()
