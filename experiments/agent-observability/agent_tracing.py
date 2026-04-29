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


tracer = Tracer()
