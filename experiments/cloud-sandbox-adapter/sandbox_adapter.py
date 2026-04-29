"""Sandbox adapter interface + two reference implementations.

The interface is intentionally minimal. Real cloud adapters (E2B, Modal,
Daytona) implement the same five methods and slot in without further loop
changes.
"""
from __future__ import annotations

import json
import shlex
import subprocess
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


@dataclass
class ExecResult:
    cmd: str
    exit_code: int
    stdout: str
    stderr: str


class SandboxAdapter(Protocol):
    def create(self) -> str: ...
    def exec(self, cmd: str) -> ExecResult: ...
    def write(self, path: str, contents: str) -> None: ...
    def read(self, path: str) -> str: ...
    def teardown(self) -> None: ...


class LocalSandbox:
    """Runs commands in the local working directory. Baseline implementation."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.cwd()
        self.sandbox_id = ""

    def create(self) -> str:
        self.sandbox_id = f"local_{uuid.uuid4().hex[:8]}"
        return self.sandbox_id

    def exec(self, cmd: str) -> ExecResult:
        proc = subprocess.run(
            cmd, shell=True, cwd=self.root, capture_output=True, text=True
        )
        return ExecResult(cmd=cmd, exit_code=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)

    def write(self, path: str, contents: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents)

    def read(self, path: str) -> str:
        return (self.root / path).read_text()

    def teardown(self) -> None:
        pass


@dataclass
class DryRunSandbox:
    """Records every operation without executing it. Output is the migration audit."""

    trace: list[dict] = field(default_factory=list)
    sandbox_id: str = ""

    def create(self) -> str:
        self.sandbox_id = f"dryrun_{uuid.uuid4().hex[:8]}"
        self.trace.append({"op": "create", "sandbox_id": self.sandbox_id})
        return self.sandbox_id

    def exec(self, cmd: str) -> ExecResult:
        self.trace.append({"op": "exec", "cmd": cmd})
        return ExecResult(cmd=cmd, exit_code=0, stdout="[dry-run]", stderr="")

    def write(self, path: str, contents: str) -> None:
        self.trace.append({"op": "write", "path": path, "bytes": len(contents)})

    def read(self, path: str) -> str:
        self.trace.append({"op": "read", "path": path})
        return ""

    def teardown(self) -> None:
        self.trace.append({"op": "teardown", "sandbox_id": self.sandbox_id})


def demo(adapter: SandboxAdapter) -> None:
    sid = adapter.create()
    print(f"sandbox_id={sid}")
    adapter.write("hello.txt", "hello from the sandbox\n")
    result = adapter.exec("ls -la hello.txt")
    print(f"  exec exit={result.exit_code}")
    if result.stdout:
        print(f"  stdout: {result.stdout.strip()}")
    contents = adapter.read("hello.txt")
    if contents:
        print(f"  read: {contents.strip()}")
    adapter.teardown()


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] != "demo":
        print("usage: sandbox_adapter.py demo [--dry-run]", file=sys.stderr)
        return 2
    if "--dry-run" in argv:
        adapter = DryRunSandbox()
        demo(adapter)
        print("\ntrace:")
        print(json.dumps(adapter.trace, indent=2))
    else:
        adapter = LocalSandbox(root=Path("/tmp"))
        demo(adapter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
