"""Generate notebooks/kaggle_llm_server.ipynb (host an OpenAI-compatible LLM on Kaggle GPU behind a tunnel).

Run: python scripts/make_kaggle_notebook.py
"""
import json
from pathlib import Path

cells = []


def md(text):
    cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': text.strip('\n').splitlines(keepends=True)})


def code(text):
    cells.append({'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [],
                  'source': text.strip('\n').splitlines(keepends=True)})


md('''
# Day 7 - host an LLM on Kaggle (OpenAI-compatible, tool calling)

Serves `Qwen2.5-7B-Instruct-AWQ` with **vLLM** and exposes it through a **Cloudflare quick tunnel**, protected by an API key.
The agent on your machine then runs with `--base-url <tunnel>/v1`.

**Before running** (notebook settings, right sidebar):
1. Accelerator: **GPU T4 x2** (or P100). Internet: **On** (needs phone verification).
2. Add-ons > Secrets: create `SERVER_API_KEY` (any long random string; label is case-sensitive) and **tick the checkbox
   next to it so it is attached to this notebook**.
   Without it a temporary key is generated and printed - then do NOT save/share this notebook's output.
3. Run all cells in order. Keep this notebook running while your agent works; the tunnel URL changes every restart.

Do not "Save version" with outputs visible if they contain the key or URL. Check Kaggle's terms before using notebooks as a server.
''')

code('''
# Installs vLLM only if it is missing. A Kaggle "Restart session" starts a fresh machine: pip packages are lost,
# so re-run this cell in every new session.
import importlib.util, subprocess, sys
if importlib.util.find_spec("vllm") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "vllm"], check=True)
import vllm
print("vllm", vllm.__version__)   # record this version in your report

# vLLM upgrades numpy to 2.x; Kaggle's preinstalled scikit-learn is built for numpy 1.x and then makes transformers (inside the
# vLLM server process) fail with "numpy.dtype size changed". Check it in a fresh process and repair it if needed.
CHECK = [sys.executable, "-c", "from sklearn.metrics import roc_curve"]
if subprocess.run(CHECK, capture_output=True).returncode != 0:
    print("scikit-learn is binary-incompatible with the new numpy: upgrading it")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "scikit-learn"], check=True)
    if subprocess.run(CHECK, capture_output=True).returncode != 0:
        print("still broken: uninstalling scikit-learn (not needed here)")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "scikit-learn"], check=True)
print("environment check done")
''')

md('''
pip prints dependency-conflict warnings for preinstalled packages (tensorflow, thinc, ...); they are harmless here.
Do **not** restart the session after the install: a restart wipes the installed packages. If you did restart, run the
install cell again before continuing.
''')

code('''
import os, re, secrets, subprocess, sys, time, urllib.request, urllib.error

MODEL = "Qwen/Qwen2.5-7B-Instruct-AWQ"   # ~5 GB, fits a single T4 (16 GB); supports tool calling
SERVED_NAME = "qwen2.5-7b-instruct"      # the --model name your client uses
PORT, MAX_LEN = 8000, 8192

KEY_GENERATED = False
try:
    from kaggle_secrets import UserSecretsClient
    API_KEY = UserSecretsClient().get_secret("SERVER_API_KEY")
except Exception as e:
    API_KEY, KEY_GENERATED = secrets.token_urlsafe(32), True
    print("Could not read Kaggle secret SERVER_API_KEY ->", type(e).__name__ + ":", e)
    print("Fix: Add-ons > Secrets, label exactly SERVER_API_KEY, and TICK it for this notebook; then Restart session.")
    print("Continuing with a temporary key generated for this session.")
print("model:", MODEL, "| gpu check:")
!nvidia-smi --query-gpu=name,memory.total --format=csv
''')

code('''
# Start the vLLM OpenAI-compatible server. The key goes through the environment (not the command line).
env = {**os.environ, "VLLM_API_KEY": API_KEY}
cmd = [sys.executable, "-m", "vllm.entrypoints.openai.api_server",
       "--model", MODEL, "--served-model-name", SERVED_NAME, "--dtype", "half",
       "--max-model-len", str(MAX_LEN), "--gpu-memory-utilization", "0.90",
       "--enable-auto-tool-choice", "--tool-call-parser", "hermes",
       "--host", "127.0.0.1", "--port", str(PORT)]
vllm_log = open("/kaggle/working/vllm.log", "w")
vllm_proc = subprocess.Popen(cmd, stdout=vllm_log, stderr=subprocess.STDOUT, env=env)


def http(path, key=True, body=None, base=f"http://127.0.0.1:{PORT}", timeout=15):
    import json
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + API_KEY
    req = urllib.request.Request(base + path, json.dumps(body).encode() if body else None, headers)
    return urllib.request.urlopen(req, timeout=timeout)


for _ in range(120):                       # up to ~20 minutes (download + load)
    if vllm_proc.poll() is not None:
        print(open("/kaggle/working/vllm.log").read()[-3000:])
        raise RuntimeError("vLLM exited; see log above (try MAX_LEN=4096 or restart the session)")
    try:
        if http("/v1/models").status == 200:
            break
    except Exception:
        pass
    time.sleep(10)
else:
    raise TimeoutError("vLLM not ready after 20 minutes; see /kaggle/working/vllm.log")

# Safety check: the endpoint must reject requests without the key.
try:
    http("/v1/models", key=False)
    raise RuntimeError("Server answered WITHOUT an API key - stop and fix before opening a tunnel")
except urllib.error.HTTPError as e:
    assert e.code in (401, 403), e.code
print("vLLM ready; unauthenticated requests are rejected.")
''')

code('''
# Public tunnel (Cloudflare quick tunnel, no account needed).
urllib.request.urlretrieve("https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", "cloudflared")
os.chmod("cloudflared", 0o755)
tun_log = open("/kaggle/working/cloudflared.log", "w")
tun_proc = subprocess.Popen(["./cloudflared", "tunnel", "--url", f"http://127.0.0.1:{PORT}", "--no-autoupdate"],
                            stdout=tun_log, stderr=subprocess.STDOUT)
PUBLIC = None
for _ in range(60):
    m = re.search(r"https://[a-z0-9-]+\\.trycloudflare\\.com", open("/kaggle/working/cloudflared.log").read())
    if m:
        PUBLIC = m.group(0)
        break
    time.sleep(2)
assert PUBLIC, "no tunnel URL; see /kaggle/working/cloudflared.log"
print("BASE URL:", PUBLIC + "/v1")
''')

code('''
# Smoke test through the public URL, including a tool call (what the agent needs).
import json
body = {"model": SERVED_NAME, "temperature": 0, "tool_choice": "auto",
        "messages": [{"role": "user", "content": "Search the documents for the definition of MCAR."}],
        "tools": [{"type": "function", "function": {"name": "search_documents", "description": "Search the textbook",
                   "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}]}
msg = json.load(http("/v1/chat/completions", body=body, base=PUBLIC, timeout=120))["choices"][0]["message"]
print("tool_calls:", msg.get("tool_calls"))
assert msg.get("tool_calls"), "model did not return a tool call"

print("\\n=== On your machine ===")
print("1) add to .env:  KAGGLE_LLM_API_KEY=<your SERVER_API_KEY value>" + ("  (temporary key: " + API_KEY + ")" if KEY_GENERATED else ""))
print(f"2) python scripts/run_agent.py --split dev --limit 2 --base-url {PUBLIC}/v1 --key-env KAGGLE_LLM_API_KEY --model {SERVED_NAME}")
''')

code('''
# Keep the session alive and watch both processes. Stop with the notebook's Interrupt button.
try:
    while True:
        if vllm_proc.poll() is not None or tun_proc.poll() is not None:
            print("a process exited; check /kaggle/working/vllm.log and cloudflared.log")
            break
        time.sleep(60)
except KeyboardInterrupt:
    pass
finally:
    for p in (tun_proc, vllm_proc):
        p.terminate()
    print("stopped")
''')

nb = {'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                                   'language_info': {'name': 'python'}}, 'nbformat': 4, 'nbformat_minor': 5}
out = Path(__file__).resolve().parents[1] / 'notebooks' / 'kaggle_llm_server.ipynb'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('wrote', out)
