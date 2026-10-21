#!/usr/bin/env python3
"""Fixed 10-turn growing conversation against a llama-server on 127.0.0.1:<port>.

Records time to first token and generation tokens/s per turn, from the stream itself.
Usage: chat_bench.py <port> <label> <out.jsonl>
"""
import json, sys, time, urllib.request

PORT, LABEL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
URL = f"http://127.0.0.1:{PORT}/v1/chat/completions"

TURNS = [
    "Summarize in three sentences why unified memory matters for running local language models.",
    "Now list five practical limits of running a 30B model on a 128 GB mini PC.",
    "Rewrite that list as advice for someone choosing between two quantization levels.",
    "Draft a short email to a friend explaining what a mixture-of-experts model is.",
    "Make the email more casual and add one concrete example.",
    "Explain the difference between prompt processing speed and generation speed.",
    "Give a worked example with numbers for a 2,000-token prompt and a 300-token reply.",
    "What would change in that example if the context grew to 16,000 tokens?",
    "Write a checklist for benchmarking two builds of the same inference engine fairly.",
    "Condense everything in this conversation into five bullet points.",
]


def wait_ready(timeout=600):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=5) as r:
                if r.status == 200:
                    return
        except Exception:
            pass
        time.sleep(2)
    sys.exit(f"server on {PORT} not ready after {timeout}s")


def one_turn(messages):
    body = json.dumps({"messages": messages, "max_tokens": 128, "temperature": 0,
                       "stream": True, "stream_options": {"include_usage": True}}).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    t0 = time.time(); first = None; text = []; ntok = 0; timings = {}
    with urllib.request.urlopen(req, timeout=600) as r:
        for line in r:
            line = line.decode().strip()
            if not line.startswith("data: ") or line == "data: [DONE]":
                continue
            ev = json.loads(line[6:])
            timings = ev.get("timings", timings)
            for ch in ev.get("choices", []):
                piece = ch.get("delta", {}).get("content")
                if piece:
                    if first is None:
                        first = time.time()
                    text.append(piece); ntok += 1
    t1 = time.time()
    gen_s = (t1 - first) if first else None
    return "".join(text), {
        "ttft_s": round(first - t0, 3) if first else None,
        "gen_tok_s": round(timings.get("predicted_per_second") or (ntok / gen_s if gen_s else 0), 2),
        "prompt_tok": timings.get("prompt_n"),
        "prompt_tok_s": round(timings.get("prompt_per_second") or 0, 1),
        "gen_tok": timings.get("predicted_n", ntok),
    }


wait_ready()
messages = [{"role": "system", "content": "You are a concise assistant."}]
with open(OUT, "a") as f:
    for i, q in enumerate(TURNS, 1):
        messages.append({"role": "user", "content": q})
        reply, m = one_turn(messages)
        messages.append({"role": "assistant", "content": reply})
        rec = {"label": LABEL, "turn": i, **m}
        f.write(json.dumps(rec) + "\n"); f.flush()
        print(json.dumps(rec), flush=True)
