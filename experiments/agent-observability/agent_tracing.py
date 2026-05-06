"""Structured span tracer for YOLO loop agent steps.

Emits one JSON record per span to a jsonl sink. Spans nest via a
ContextVar so callers don't have to thread parent ids through every call.
"""
from __future__ import annotations

import contextvars
import hashlib
import json
import os
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator, TextIO


_current_span: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "current_span", default=None
)

# Per-token pricing in USD/1M tokens. Replace with real values per model.
_PRICING: dict[str, tuple[float, float]] = {
    "claude-opus-4-7": (15.0, 75.0),
    "claude-haiku-4-5": (1.0, 5.0),
    "claude.messages.create": (15.0, 75.0),  # default to opus rates if unspecified
    "gpt-5-codex": (5.0, 20.0),
    "gemini-1.5-pro": (3.5, 10.5),
}


def _cost_usd(tool: str, token_in: int, token_out: int) -> float:
    rates = _PRICING.get(tool, (0.0, 0.0))
    return round((token_in * rates[0] + token_out * rates[1]) / 1_000_000, 6)


def _short_hash(value: Any) -> str:
    if value is None:
        return ""
    s = value if isinstance(value, str) else json.dumps(value, sort_keys=True, default=str)
    return hashlib.sha256(s.encode()).hexdigest()[:12]


@dataclass
class Span:
    span_id: str
    parent_id: str | None
    name: str
    ts_start: float
    tool: str = ""
    token_in: int = 0
    token_out: int = 0
    input_hash: str = ""
    output_hash: str = ""
    status: str = "ok"
    error: str = ""
    extra: dict[str, Any] = field(default_factory=dict)
    ts_end: float = 0.0

    def to_record(self) -> dict[str, Any]:
        latency_ms = int((self.ts_end - self.ts_start) * 1000) if self.ts_end else 0
        return {
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "tool": self.tool,
            "ts_start": self.ts_start,
            "ts_end": self.ts_end,
            "latency_ms": latency_ms,
            "token_in": self.token_in,
            "token_out": self.token_out,
            "cost_usd": _cost_usd(self.tool, self.token_in, self.token_out),
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "status": self.status,
            "error": self.error,
            **({"extra": self.extra} if self.extra else {}),
        }


class Tracer:
    def __init__(self, sink: str | Path | TextIO | None = None) -> None:
        if sink is None:
            sink = os.environ.get("AGENT_TRACE_FILE", "traces.jsonl")
        if isinstance(sink, (str, Path)):
            self._path = Path(sink)
            self._fh: TextIO | None = None
        else:
            self._path = None
            self._fh = sink

    def _emit(self, record: dict[str, Any]) -> None:
        line = json.dumps(record) + "\n"
        if self._fh is not None:
            self._fh.write(line)
            self._fh.flush()
        else:
            with self._path.open("a") as f:
                f.write(line)

    @contextmanager
    def span(self, name: str) -> Iterator[Span]:
        span_id = uuid.uuid4().hex[:16]
        parent_id = _current_span.get()
        s = Span(span_id=span_id, parent_id=parent_id, name=name, ts_start=time.time())
        token = _current_span.set(span_id)
        try:
            yield s
        except Exception as exc:
            s.status = "error"
            s.error = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            s.ts_end = time.time()
            _current_span.reset(token)
            self._emit(s.to_record())

    def hash(self, value: Any) -> str:
        return _short_hash(value)


    def summary(self) -> dict[str, Any]:
        """In-memory aggregate over the current sink path. Useful when the
        caller wants live stats without spawning a separate aggregator."""
        if self._path is None or not self._path.exists():
            return {"total_spans": 0, "tools": {}}
        total = 0
        tools: dict[str, dict[str, Any]] = {}
        with self._path.open() as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                total += 1
                tool = r.get("tool") or "(no-tool)"
                t = tools.setdefault(tool, {"calls": 0, "token_in": 0, "token_out": 0, "cost_usd": 0.0, "errors": 0})
                t["calls"] += 1
                t["token_in"] += r.get("token_in", 0)
                t["token_out"] += r.get("token_out", 0)
                t["cost_usd"] += r.get("cost_usd", 0.0)
                if r.get("status") == "error":
                    t["errors"] += 1
        return {"total_spans": total, "tools": tools}


tracer = Tracer()
