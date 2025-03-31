# backend/tests/run_all_tests.py

import subprocess
import time
import pytest
import signal
import os
import sys

def start_backend():
    # Elindítjuk a backendet uvicorn-nal alfolyamatban
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )

def stop_backend(process):
    # Leállítjuk a backendet
    if os.name == 'nt':
        process.send_signal(signal.CTRL_BREAK_EVENT)
    else:
        process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

if __name__ == "__main__":
    print("🔧 Indul a backend szerver a tesztekhez...")
    backend_process = start_backend()
    time.sleep(2)  # várunk, hogy legyen ideje elindulni

    try:
        exit_code = pytest.main(["-v"])
    finally:
        print("🛑 Leállítjuk a backend szervert...")
        stop_backend(backend_process)

    sys.exit(exit_code)
