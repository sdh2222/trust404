"""End-to-end CLI tests for tools/ensemble.py."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

from detector.submission import validate_against_schema
from tests.detector.conftest import REPO_ROOT

TIER0 = REPO_ROOT / "cases" / "tier0_judge"
BENCH_SCHEMA = REPO_ROOT / "baybench" / "schema" / "result.schema.json"

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node is missing")

EXPECTED_VERDICTS = {
    "P1_StandardToken_sol.sol": "BENIGN",
    "P4_CappedMint_sol.sol": "BENIGN",
    "P2_HiddenMint_sol.sol": "MALICIOUS",
    "P3_Honeypot_sol.sol": "MALICIOUS",
    "P5_DelegatecallBackdoor_sol.sol": "MALICIOUS",
}


@pytest.fixture
def flat_tier0(tmp_path: Path) -> Path:
    dest = tmp_path / "in"
    dest.mkdir()
    for src in sorted(TIER0.glob("*/*.sol")):
        shutil.copy2(src, dest / src.name)
    return dest


def _run_ensemble(
    in_dir: Path,
    extra: list[str] | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, "tools/ensemble.py", str(in_dir)]
    if extra:
        cmd.extend(extra)
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )


def _assert_tier0_verdicts(rows: list[dict]) -> None:
    assert len(rows) == 5
    by_file = {row["file"]: row["verdict"] for row in rows}
    assert by_file == EXPECTED_VERDICTS


def test_judge_mode_public_set(flat_tier0: Path, noexit_dist: Path) -> None:
    proc = _run_ensemble(flat_tier0)
    assert proc.returncode == 0, proc.stderr
    rows = json.loads(proc.stdout)
    assert isinstance(rows, list)
    validate_against_schema(rows)
    _assert_tier0_verdicts(rows)
    assert proc.stdout.strip().startswith("[")
    json.loads(proc.stdout)
    assert proc.stdout.count("\n[") <= 1
    assert "[ensemble] detector: 5 rows" in proc.stderr
    assert "[ensemble] noexit: 5 rows" in proc.stderr
    assert "DEGRADED" not in proc.stderr


def test_judge_mode_deterministic(flat_tier0: Path, noexit_dist: Path) -> None:
    first = _run_ensemble(flat_tier0)
    second = _run_ensemble(flat_tier0)
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert first.stdout == second.stdout


def test_bench_mode_deterministic(
    flat_tier0: Path, tmp_path: Path, noexit_dist: Path
) -> None:
    first_path = tmp_path / "a" / "results.json"
    second_path = tmp_path / "b" / "results.json"
    first_path.parent.mkdir()
    second_path.parent.mkdir()
    first = _run_ensemble(flat_tier0, extra=["--bench-out", str(first_path)])
    second = _run_ensemble(flat_tier0, extra=["--bench-out", str(second_path)])
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert first_path.read_bytes() == second_path.read_bytes()


def test_judge_mode_noexit_dead_is_degraded(
    flat_tier0: Path, noexit_dist: Path
) -> None:
    env = {**os.environ, "ENSEMBLE_NODE": "/nonexistent/node"}
    proc = _run_ensemble(flat_tier0, env=env)
    assert proc.returncode == 0, proc.stderr
    rows = json.loads(proc.stdout)
    validate_against_schema(rows)
    assert "DEGRADED: noexit" in proc.stderr
    _assert_tier0_verdicts(rows)


def test_judge_mode_detector_dead_is_degraded(
    flat_tier0: Path, tmp_path: Path, noexit_dist: Path
) -> None:
    shim = tmp_path / "bad_python"
    shim.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    shim.chmod(0o755)
    env = {**os.environ, "ENSEMBLE_PYTHON": str(shim)}
    proc = _run_ensemble(flat_tier0, env=env)
    assert proc.returncode == 0, proc.stderr
    rows = json.loads(proc.stdout)
    validate_against_schema(rows)
    assert "DEGRADED: detector" in proc.stderr
    _assert_tier0_verdicts(rows)


def test_judge_mode_engines_flag_detector_only_matches_detector_cli(
    flat_tier0: Path,
    noexit_dist: Path,
) -> None:
    ens = _run_ensemble(flat_tier0, extra=["--engines", "detector"])
    assert ens.returncode == 0, ens.stderr
    ens_rows = json.loads(ens.stdout)
    det = subprocess.run(
        [sys.executable, "-m", "detector.cli", str(flat_tier0)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    assert det.returncode == 0, det.stderr
    det_rows = json.loads(det.stdout)
    ens_by = {row["file"]: row for row in ens_rows}
    det_by = {row["file"]: row for row in det_rows}
    assert set(ens_by) == set(det_by)
    for name in ens_by:
        assert ens_by[name]["verdict"] == det_by[name]["verdict"]
        assert ens_by[name]["reasons"] == det_by[name]["reasons"]
        assert ens_by[name]["evidence"] == det_by[name]["evidence"]


def test_bench_mode_writes_schema_valid_results(
    flat_tier0: Path, tmp_path: Path, noexit_dist: Path
) -> None:
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    bench_path = out_dir / "results.json"
    proc = _run_ensemble(flat_tier0, extra=["--bench-out", str(bench_path)])
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == ""
    assert bench_path.is_file()
    payload = json.loads(bench_path.read_text(encoding="utf-8"))
    schema = json.loads(BENCH_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(payload, schema)
    assert payload["tool"]["name"] == "ensemble"
    results = payload["results"]
    assert len(results) == 5
    title = {
        "P1_StandardToken_sol.sol": "Benign",
        "P4_CappedMint_sol.sol": "Benign",
        "P2_HiddenMint_sol.sol": "Malicious",
        "P3_Honeypot_sol.sol": "Malicious",
        "P5_DelegatecallBackdoor_sol.sol": "Malicious",
    }
    by_file = {row["file"]: row for row in results}
    for name, verdict in title.items():
        assert by_file[name]["verdict"] == verdict

    det_path = tmp_path / "detector.json"
    det = subprocess.run(
        [
            sys.executable,
            "-m",
            "detector.cli",
            str(flat_tier0),
            str(det_path),
            "--no-summary",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    assert det.returncode == 0, det.stderr
    det_payload = json.loads(det_path.read_text(encoding="utf-8"))
    det_by = {row["file"]: row for row in det_payload["results"]}
    for name, row in by_file.items():
        det_findings = det_by[name].get("findings") or []
        ens_findings = row.get("findings") or []
        for finding in det_findings:
            assert finding in ens_findings


def test_empty_dir_prints_empty_array(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    proc = _run_ensemble(empty)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "[]\n"


def test_usage_error() -> None:
    proc = subprocess.run(
        [sys.executable, "tools/ensemble.py"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert proc.returncode == 2
    assert proc.stdout == "[]\n"
