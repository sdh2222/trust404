import json
import os
import shutil
import subprocess
from pathlib import Path

import jsonschema
import pytest

REPO = Path(__file__).resolve().parents[2]
NOEXIT = REPO / "noexit"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None or shutil.which("npm") is None,
    reason="node/npm not installed",
)


def test_upstream_file_names_source() -> None:
    upstream = NOEXIT / "UPSTREAM"
    assert upstream.is_file()
    assert "cbcef71a" in upstream.read_text(encoding="utf-8")


def test_vendored_set_is_slim() -> None:
    entries = {p.name for p in NOEXIT.iterdir() if p.name not in {"node_modules", "dist"}}
    assert entries == {
        ".dockerignore",
        ".gitignore",
        "README.md",
        "UPSTREAM",
        "package-lock.json",
        "package.json",
        "run.sh",
        "src",
        "tsconfig.json",
    }
    ts_files = list((NOEXIT / "src").glob("*.ts"))
    assert len(ts_files) == 16


@pytest.fixture(scope="session")
def built_dist() -> Path:
    if not (NOEXIT / "node_modules").exists():
        subprocess.run(
            ["npm", "ci", "--ignore-scripts"],
            check=True,
            capture_output=True,
            text=True,
            cwd=NOEXIT,
        )
    subprocess.run(
        ["npx", "tsc", "-p", "tsconfig.json"],
        check=True,
        capture_output=True,
        text=True,
        cwd=NOEXIT,
    )
    dist = NOEXIT / "dist"
    assert (dist / "cli.js").is_file()
    assert (dist / "baybench.js").is_file()
    return dist


def test_judge_cli_on_public_set(built_dist: Path, tmp_path: Path) -> None:
    tmp_in = tmp_path / "in"
    tmp_in.mkdir()
    for src in (REPO / "cases" / "tier0_judge").glob("*/*.sol"):
        shutil.copy(src, tmp_in / src.name.replace("_sol.sol", ".sol"))
    proc = subprocess.run(
        ["node", "dist/cli.js", "judge", str(tmp_in)],
        capture_output=True,
        check=True,
        timeout=300,
        text=True,
        cwd=NOEXIT,
    )
    stdout = proc.stdout
    rows = json.loads(stdout)
    assert isinstance(rows, list) and rows
    schema = json.loads(
        (REPO / "detector" / "schema" / "judge.schema.json").read_text(encoding="utf-8")
    )
    jsonschema.validate(rows, schema)
    by_file = {row["file"]: row["verdict"] for row in rows}
    assert by_file == {
        "P1_StandardToken.sol": "BENIGN",
        "P2_HiddenMint.sol": "MALICIOUS",
        "P3_Honeypot.sol": "MALICIOUS",
        "P4_CappedMint.sol": "BENIGN",
        "P5_DelegatecallBackdoor.sol": "MALICIOUS",
    }
    assert stdout.strip().startswith("[")


def test_baybench_adapter_on_public_set(built_dist: Path, tmp_path: Path) -> None:
    tmp_in = tmp_path / "in"
    tmp_in.mkdir()
    for src in (REPO / "cases" / "tier0_judge").glob("*/*.sol"):
        shutil.copy(src, tmp_in / src.name.replace("_sol.sol", ".sol"))
    results_path = tmp_path / "results.json"
    subprocess.run(
        ["node", "dist/baybench.js", str(tmp_in), str(results_path)],
        capture_output=True,
        check=True,
        timeout=300,
        text=True,
        cwd=NOEXIT,
    )
    assert results_path.is_file()
    with results_path.open(encoding="utf-8") as fh:
        obj = json.load(fh)
    schema = json.loads(
        (REPO / "baybench" / "schema" / "result.schema.json").read_text(encoding="utf-8")
    )
    jsonschema.validate(obj, schema)
    assert obj["tool"]["name"] == "noexit"
    assert len(obj["results"]) == 5
