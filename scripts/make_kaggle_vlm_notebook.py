"""Derive notebooks/kaggle_vlm_server.ipynb (vision-language model) from the working text notebook.

Run after scripts/make_kaggle_notebook.py:  python scripts/make_kaggle_vlm_notebook.py
Differences from the text notebook: Qwen2.5-VL AWQ model, longer context for image tokens, a per-prompt image limit,
fewer concurrent sequences (memory) and an image-reading smoke test.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
nb = json.loads((ROOT / 'notebooks' / 'kaggle_llm_server.ipynb').read_text(encoding='utf-8'))


def sub(cell, old, new):
    src = ''.join(cell['source'])
    assert old in src, f'missing text to replace: {old[:50]!r}'
    cell['source'] = src.replace(old, new).splitlines(keepends=True)


def find(marker):
    return next(c for c in nb['cells'] if marker in ''.join(c['source']))


sub(find('# Day 7 - host an LLM'), '# Day 7 - host an LLM on Kaggle (OpenAI-compatible, tool calling)',
    '# Day 7 (advanced) - host a vision-language model on Kaggle (OpenAI-compatible, images + tool calling)')
sub(find('Serves `Qwen2.5-7B'), 'Serves `Qwen2.5-7B-Instruct-AWQ`', 'Serves `Qwen2.5-VL-7B-Instruct-AWQ` (reads page images, tables and charts)')

cfg = find('MODEL = "Qwen/Qwen2.5-7B-Instruct-AWQ"')
sub(cfg, 'MODEL = "Qwen/Qwen2.5-7B-Instruct-AWQ"   # ~5 GB, fits a single T4 (16 GB); supports tool calling',
    'MODEL = "Qwen/Qwen2.5-VL-7B-Instruct-AWQ"   # ~6 GB; fits one T4 (16 GB); images + tool calling')
sub(cfg, 'SERVED_NAME = "qwen2.5-7b-instruct"', 'SERVED_NAME = "qwen2.5-vl-7b-instruct"')
sub(cfg, 'PORT, MAX_LEN = 8000, 8192', 'PORT, MAX_LEN = 8000, 12288   # a page image costs thousands of tokens')

start = find('"--enable-auto-tool-choice"')
sub(start, '"--enable-auto-tool-choice", "--tool-call-parser", "hermes",',
    '"--enable-auto-tool-choice", "--tool-call-parser", "hermes",\n'
    '       "--limit-mm-per-prompt", \'{"image": 4}\', "--max-num-seqs", "4",')

smoke = find('# Smoke test through the public URL')
sub(smoke, '# Smoke test through the public URL, including a tool call (what the agent needs).\nimport json\n', '''# Smoke test through the public URL: (1) read an image, (2) tool call.
import base64, io, json
from PIL import Image, ImageDraw
img = Image.new("RGB", (480, 160), "white")
ImageDraw.Draw(img).text((20, 60), "TOTAL SALES 4242 UNITS", fill="black")
img = img.resize((960, 320))
buf = io.BytesIO(); img.save(buf, "PNG")
vbody = {"model": SERVED_NAME, "temperature": 0, "max_tokens": 40, "messages": [{"role": "user", "content": [
    {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()}},
    {"type": "text", "text": "What number is written in the image? Answer with the number only."}]}]}
reply = json.load(http("/v1/chat/completions", body=vbody, base=PUBLIC, timeout=180))["choices"][0]["message"]["content"]
print("vision reply:", reply)
assert "4242" in reply, "the model did not read the image correctly (fp16 issue? try another dtype/model)"
''')
sub(smoke, '''body = {"model": SERVED_NAME, "temperature": 0, "tool_choice": "auto",''', 'body = {"model": SERVED_NAME, "temperature": 0, "tool_choice": "auto",')
sub(smoke, '''msg = json.load(http("/v1/chat/completions", body=body, base=PUBLIC, timeout=120))["choices"][0]["message"]
print("tool_calls:", msg.get("tool_calls"))
assert msg.get("tool_calls"), "model did not return a tool call"
''', '''# Qwen2.5-VL is less inclined to call tools on its own, so test both modes. The agent uses "required" on its first turn
# (--force-first-search); only that mode must pass.
for mode in ("auto", "required"):
    msg = json.load(http("/v1/chat/completions", body={**body, "tool_choice": mode}, base=PUBLIC, timeout=120))["choices"][0]["message"]
    print(f"tool_choice={mode}: tool_calls =", msg.get("tool_calls"), "| content =", repr((msg.get("content") or "")[:200]))
assert msg.get("tool_calls"), 'tool_choice="required" did not return a tool call: check /kaggle/working/vllm.log'
''')
out = ROOT / 'notebooks' / 'kaggle_vlm_server.ipynb'
out.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('wrote', out)
