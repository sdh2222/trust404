"""Static checks on the root ensemble Dockerfile."""

from __future__ import annotations

import json
from pathlib import Path

from tests.detector.conftest import REPO_ROOT

DOCKERFILE = REPO_ROOT / "Dockerfile"
DOCKERIGNORE = REPO_ROOT / ".dockerignore"

_ALLOWED_NOEXIT_SOURCES = {
    "noexit/package.json",
    "noexit/package-lock.json",
    "noexit/tsconfig.json",
    "noexit/run.sh",
    "noexit/src",
}


def _instructions(text: str) -> list[str]:
    logical: list[str] = []
    buf = ""
    continuing = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if not continuing:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
        if line.endswith("\\"):
            piece = line[:-1].strip()
            buf = f"{buf} {piece}".strip() if continuing else piece
            continuing = True
            continue
        piece = line.strip()
        if continuing:
            logical.append(f"{buf} {piece}".strip())
            buf = ""
            continuing = False
            continue
        logical.append(piece)
    if continuing and buf:
        logical.append(buf)
    return logical


def _copy_sources(inst: str) -> list[str]:
    tokens = inst.split()[1:]
    if not tokens:
        return []
    return tokens[:-1]


def test_root_dockerfile_is_thin_ensemble_layer() -> None:
    text = DOCKERFILE.read_text(encoding="utf-8")
    inst = _instructions(text)
    assert inst, "Dockerfile missing or empty after comment strip"
    assert inst[0] == "ARG BASE=ghcr.io/sdh2222/trust404-detector:latest"
    assert inst[1] == "FROM ${BASE}"
    assert sum(1 for line in inst if line.startswith("FROM ")) == 1

    blob = "\n".join(inst)
    assert "solc-select" not in blob
    assert "pip install" not in blob
    assert "COPY vendor/" not in blob
    assert "npm ci --ignore-scripts" in blob
    assert "npx tsc -p tsconfig.json" in blob
    assert "npm prune --omit=dev" in blob
    assert "COPY tools/ensemble.py /app/tools/ensemble.py" in blob

    chmod_lines = [line for line in inst if "chmod -R a+rX" in line]
    assert chmod_lines, "missing chmod -R a+rX"
    assert any("/app/noexit" in line and "/opt/detector-home" in line for line in chmod_lines)

    assert "COPY noexit/samples" not in blob
    assert "COPY noexit/web" not in blob
    copy_lines = [line for line in inst if line.startswith("COPY ")]
    for line in copy_lines:
        for src in _copy_sources(line):
            if src == "noexit" or src == "noexit/" or src.startswith("noexit"):
                assert src in _ALLOWED_NOEXIT_SOURCES, line

    entry = [line for line in inst if line.startswith("ENTRYPOINT ")]
    assert len(entry) == 1
    assert json.loads(entry[0][len("ENTRYPOINT ") :]) == [
        "python3",
        "/app/tools/ensemble.py",
    ]
    cmd = [line for line in inst if line.startswith("CMD ")]
    assert len(cmd) == 1
    assert json.loads(cmd[0][len("CMD ") :]) == ["/input"]

    assert not any(line.startswith("USER ") for line in inst)
    for line in inst:
        if "apt-get install" in line:
            assert "--no-install-recommends" in line


def test_dockerignore_excludes_node_modules() -> None:
    lines = [
        ln.strip()
        for ln in DOCKERIGNORE.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    assert "node_modules/" in lines
    assert ".venv/" in lines
    assert ".git/" in lines
    assert ".bench_work/" in lines
