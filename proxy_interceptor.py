import sys
import subprocess
import threading
import os
import json

# When frozen by PyInstaller, sys.executable is the real exe path in d:\tt\tunnet-runtime.exe
if getattr(sys, 'frozen', False):
    EXE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    EXE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(EXE_DIR, "captured_ipc.jsonl")
REAL_NODES_FILE = os.path.join(EXE_DIR, "real_captured_nodes.json")
CREDENTIALS_FILE = os.path.join(EXE_DIR, "real_credentials.json")
CORE_EXE = os.path.join(EXE_DIR, "tunnet-runtime-core.exe")

def log(tag, data_str):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{tag}: {data_str}\n")
    except Exception:
        pass

def parse_and_save_data(line_str):
    try:
        obj = json.loads(line_str)
        # Check if it is initialize params from client
        if obj.get("method") == "initialize" and "params" in obj:
            p = obj["params"]
            with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
                json.dump(p, f, indent=2, ensure_ascii=False)
            log("[SAVED_CREDENTIALS]", json.dumps(p))

        # Check if it is response with entry_nodes / hosts / access
        if "result" in obj and isinstance(obj["result"], dict):
            res = obj["result"]
            if any(k in res for k in ["entry_nodes", "hosts", "access", "root_domains"]):
                with open(REAL_NODES_FILE, "w", encoding="utf-8") as f:
                    json.dump(res, f, indent=2, ensure_ascii=False)
                log("[SAVED_NODES]", json.dumps(res))
    except Exception:
        pass

if not os.path.exists(CORE_EXE):
    # fallback search
    CORE_EXE = r"d:\tt\tunnet-runtime-core.exe"

proc = subprocess.Popen(
    [CORE_EXE] + sys.argv[1:],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd=EXE_DIR,
    bufsize=0
)

def pipe_stdin():
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            break
        try:
            line_str = line.decode('utf-8', errors='ignore').strip()
            log("[CLIENT->RUNTIME]", line_str)
            parse_and_save_data(line_str)
        except Exception:
            pass
        try:
            proc.stdin.write(line)
            proc.stdin.flush()
        except Exception:
            break

def pipe_stderr():
    while True:
        line = proc.stderr.readline()
        if not line:
            break
        sys.stderr.buffer.write(line)
        sys.stderr.buffer.flush()

t_in = threading.Thread(target=pipe_stdin, daemon=True)
t_err = threading.Thread(target=pipe_stderr, daemon=True)
t_in.start()
t_err.start()

while True:
    line = proc.stdout.readline()
    if not line:
        break
    try:
        line_str = line.decode('utf-8', errors='ignore').strip()
        log("[RUNTIME->CLIENT]", line_str)
        parse_and_save_data(line_str)
    except Exception:
        pass
    try:
        sys.stdout.buffer.write(line)
        sys.stdout.buffer.flush()
    except Exception:
        break

proc.wait()
