#!/usr/bin/env python3
"""Two-engine merge entry point: detector + noexit → one judge array or BAYBENCH results.json."""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
logger = logging.getLogger("ensemble")

_KNOWN_ENGINES = ("detector", "noexit")
_OUTPUT_DIR = "/output"

_KNOWN_VERDICTS = ("MALICIOUS", "BENIGN", "UNCERTAIN")
_BOTH_FAILED = "Both engines failed or timed out; no verdict could be produced."
_NO_FILE_VERDICT = "No engine produced a verdict for this file."
_ABSTAIN_REASON = (
    "Engines abstained or disagreed without evidence; no confident verdict."
)
_DOWNGRADE_REASON = (
    "An engine flagged this file as malicious but produced no code location; "
    "downgraded to UNCERTAIN."
)
_OPTIONAL_KEYS = ("risk_level", "risk_type", "confidence")


def norm_verdict(value: object) -> str:
    if not isinstance(value, str):
        return "UNCERTAIN"
    upper = value.upper()
    if upper in _KNOWN_VERDICTS:
        return upper
    return "UNCERTAIN"


def effective_budget(
    mode: str, budget_flag: float | None, env_budget: str | None
) -> float | None:
    if budget_flag is not None:
        return budget_flag
    if env_budget:
        return float(env_budget)
    match mode:
        case "judge":
            return 540.0
        case "bench":
            return None
        case _ as unreachable:
            raise AssertionError(f"unreachable mode: {unreachable!r}")


def decide(d: str | None, n: str | None) -> str:
    d_n = None if d is None else norm_verdict(d)
    n_n = None if n is None else norm_verdict(n)
    match (d_n, n_n):
        case ("MALICIOUS", _) | (_, "MALICIOUS"):
            return "MALICIOUS"
        case ("BENIGN", _):
            return "BENIGN"
        case ("UNCERTAIN", _) | (None, "BENIGN") | (None, "UNCERTAIN") | (None, None):
            return "UNCERTAIN"
        case _ as unreachable:
            raise AssertionError(f"unreachable decide pair: {unreachable!r}")


def clean_evidence(items: object) -> list[dict]:
    cleaned: list[dict] = []
    if not isinstance(items, list):
        return cleaned
    for raw in items:
        if not isinstance(raw, dict):
            continue
        item: dict = {}
        function = raw.get("function")
        if isinstance(function, str) and function:
            item["function"] = function
        line = raw.get("line")
        if isinstance(line, int) and line >= 1:
            item["line"] = line
        if item and item not in cleaned:
            cleaned.append(item)
    return cleaned


def _reasons_from(row: dict | None) -> list[str]:
    if row is None:
        return []
    raw = row.get("reasons")
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        if isinstance(item, str) and item and item not in out:
            out.append(item)
    return out


def _union_reasons(rows: list[dict | None]) -> list[str]:
    out: list[str] = []
    for row in rows:
        for reason in _reasons_from(row):
            if reason not in out:
                out.append(reason)
    return out


def _union_evidence(rows: list[dict | None]) -> list[dict]:
    out: list[dict] = []
    for row in rows:
        if row is None:
            continue
        for item in clean_evidence(row.get("evidence")):
            if item not in out:
                out.append(item)
    return out


def _copy_optional(out: dict, voters: list[dict]) -> None:
    for key in _OPTIONAL_KEYS:
        for row in voters:
            if key in row:
                out[key] = row[key]
                break


def _normalize_judge_row(row: dict) -> dict:
    file_name = row.get("file")
    out = {
        "file": file_name if isinstance(file_name, str) else "",
        "verdict": norm_verdict(row.get("verdict")),
        "reasons": _reasons_from(row),
        "evidence": clean_evidence(row.get("evidence")),
    }
    _copy_optional(out, [row])
    return out


def _empty_uncertain(file: str, reasons: list[str]) -> dict:
    return {
        "file": file,
        "verdict": "UNCERTAIN",
        "reasons": list(reasons),
        "evidence": [],
    }


def merge_judge(file: str, d_row: dict | None, n_row: dict | None) -> dict:
    if d_row is None and n_row is None:
        return _empty_uncertain(file, [_NO_FILE_VERDICT])
    d_v = None if d_row is None else norm_verdict(d_row.get("verdict"))
    n_v = None if n_row is None else norm_verdict(n_row.get("verdict"))
    final = decide(d_v, n_v)
    voters: list[dict] = []
    if d_row is not None and d_v == final:
        voters.append(d_row)
    if n_row is not None and n_v == final:
        voters.append(n_row)
    if not voters:
        voters = [row for row in (d_row, n_row) if row is not None]
    if final == "UNCERTAIN":
        reasons = _union_reasons([d_row, n_row])
    else:
        reasons = _union_reasons(voters)
    evidence = _union_evidence(voters)
    if final == "MALICIOUS" and not evidence:
        final = "UNCERTAIN"
        reasons = [_DOWNGRADE_REASON, *[r for r in reasons if r != _DOWNGRADE_REASON]]
    if final == "UNCERTAIN" and not reasons:
        reasons = [_ABSTAIN_REASON]
    out = {
        "file": file,
        "verdict": final,
        "reasons": reasons,
        "evidence": evidence,
    }
    _copy_optional(out, voters)
    return out


def _bench_verdict(row: dict | None) -> str | None:
    if row is None:
        return None
    raw = row.get("verdict")
    if not isinstance(raw, str):
        return None
    return raw


def _bench_findings(row: dict | None) -> list[dict]:
    if row is None:
        return []
    raw = row.get("findings")
    if not isinstance(raw, list):
        return []
    out: list[dict] = []
    for item in raw:
        if isinstance(item, dict) and item not in out:
            out.append(item)
    return out


def merge_bench(file: str, d_row: dict | None, n_row: dict | None) -> dict:
    d_raw = _bench_verdict(d_row)
    n_raw = _bench_verdict(n_row)
    d_u = None if d_raw is None else d_raw.upper()
    n_u = None if n_raw is None else n_raw.upper()
    final = decide(d_u, n_u)
    title = final.title()
    findings = _bench_findings(d_row)
    for item in _bench_findings(n_row):
        if item not in findings:
            findings.append(item)
    out: dict = {"file": file, "verdict": title, "findings": findings}
    if title == "Uncertain":
        d_reason = d_row.get("reason") if isinstance(d_row, dict) else None
        n_reason = n_row.get("reason") if isinstance(n_row, dict) else None
        if isinstance(d_reason, str) and d_reason:
            out["reason"] = d_reason
        elif isinstance(n_reason, str) and n_reason:
            out["reason"] = n_reason
        else:
            out["reason"] = "both engines abstained"
    return out


def merge_all(
    files: list[str],
    detector_rows: dict[str, dict] | None,
    noexit_rows: dict[str, dict] | None,
) -> list[dict]:
    detector_alive = detector_rows is not None
    noexit_alive = noexit_rows is not None
    if not detector_alive and not noexit_alive:
        return [_empty_uncertain(name, [_BOTH_FAILED]) for name in files]
    if detector_alive and not noexit_alive:
        return _passthrough_judge(files, detector_rows)
    if noexit_alive and not detector_alive:
        return _passthrough_judge(files, noexit_rows)
    assert detector_rows is not None and noexit_rows is not None
    rows: list[dict] = []
    for name in files:
        d_row = detector_rows.get(name)
        n_row = noexit_rows.get(name)
        rows.append(merge_judge(name, d_row, n_row))
    return rows


def _passthrough_judge(files: list[str], engine_rows: dict[str, dict]) -> list[dict]:
    out: list[dict] = []
    for name in files:
        row = engine_rows.get(name)
        if row is None:
            out.append(_empty_uncertain(name, [_NO_FILE_VERDICT]))
            continue
        normalised = _normalize_judge_row(row)
        normalised["file"] = name
        if normalised["verdict"] == "MALICIOUS" and not normalised["evidence"]:
            normalised["verdict"] = "UNCERTAIN"
            reasons = normalised["reasons"]
            normalised["reasons"] = [
                _DOWNGRADE_REASON,
                *[r for r in reasons if r != _DOWNGRADE_REASON],
            ]
        if normalised["verdict"] == "UNCERTAIN" and not normalised["reasons"]:
            normalised["reasons"] = [_ABSTAIN_REASON]
        out.append(normalised)
    return out


def _configure_logging() -> None:
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[ensemble] %(message)s",
        force=True,
    )


def _auto_mode() -> str:
    if os.path.isdir(_OUTPUT_DIR) and os.access(_OUTPUT_DIR, os.W_OK):
        return "bench"
    return "judge"


def parse_engines(raw: str) -> list[str]:
    selected: list[str] = []
    seen: dict[str, None] = {}
    for part in raw.split(","):
        name = part.strip().lower()
        if not name:
            continue
        if name not in _KNOWN_ENGINES:
            logger.warning("unknown engine %r; ignoring", name)
            continue
        if name not in seen:
            seen[name] = None
            selected.append(name)
    if not selected:
        return ["detector", "noexit"]
    return [name for name in _KNOWN_ENGINES if name in seen]


def list_judge_files(input_dir: Path) -> list[str]:
    names: list[str] = []
    try:
        children = list(input_dir.iterdir())
    except OSError:
        return []
    for path in children:
        if path.is_file() and path.suffix == ".sol":
            names.append(path.name)
    names.sort()
    return names


def _index_rows(rows: list[object]) -> dict[str, dict]:
    by_file: dict[str, dict] = {}
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("file"), str):
            key = row["file"]
            if key not in by_file:
                by_file[key] = row
    return by_file


def _tool_version(payload: dict | None) -> str:
    if not isinstance(payload, dict):
        return ""
    tool = payload.get("tool")
    if not isinstance(tool, dict):
        return ""
    version = tool.get("version")
    if isinstance(version, str):
        return version
    return ""


def _engine_command(
    name: str,
    mode: str,
    input_dir: Path,
    python: str,
    node: str,
    detector_budget_s: float,
    tmp: Path | None,
) -> list[str]:
    match (name, mode):
        case ("detector", "judge"):
            return [
                python,
                "-m",
                "detector.cli",
                str(input_dir),
                "--budget",
                str(detector_budget_s),
            ]
        case ("noexit", "judge"):
            return [node, str(ROOT / "noexit" / "dist" / "cli.js"), "judge", str(input_dir)]
        case ("detector", "bench"):
            assert tmp is not None
            return [
                python,
                "-m",
                "detector.cli",
                str(input_dir),
                str(tmp / "detector.json"),
                "--no-summary",
            ]
        case ("noexit", "bench"):
            assert tmp is not None
            return [
                node,
                str(ROOT / "noexit" / "dist" / "baybench.js"),
                str(input_dir),
                str(tmp / "noexit.json"),
            ]
        case _ as unreachable:
            raise AssertionError(f"unreachable engine command: {unreachable!r}")


def _stderr_tail(raw: str | None) -> str:
    if not raw:
        return ""
    return raw[-4000:]


def _run_one_engine(
    name: str,
    cmd: list[str],
    *,
    mode: str,
    budget_s: float | None,
    env: dict[str, str],
    tmp: Path | None,
    n_judge_files: int,
) -> dict:
    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=budget_s,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - t0
        err = exc.stderr
        if isinstance(err, bytes):
            err = err.decode("utf-8", errors="replace")
        return {
            "name": name,
            "alive": False,
            "by_file": {},
            "bench_obj": None,
            "elapsed_s": elapsed,
            "why": f"timeout after {budget_s:g}s",
            "stderr_tail": _stderr_tail(err if isinstance(err, str) else None),
        }
    except FileNotFoundError:
        return {
            "name": name,
            "alive": False,
            "by_file": {},
            "bench_obj": None,
            "elapsed_s": time.monotonic() - t0,
            "why": "exit 127",
            "stderr_tail": "",
        }
    except OSError as exc:
        return {
            "name": name,
            "alive": False,
            "by_file": {},
            "bench_obj": None,
            "elapsed_s": time.monotonic() - t0,
            "why": f"exit {exc.errno if exc.errno is not None else 1}",
            "stderr_tail": "",
        }
    elapsed = time.monotonic() - t0
    tail = _stderr_tail(proc.stderr)
    if proc.returncode != 0:
        return {
            "name": name,
            "alive": False,
            "by_file": {},
            "bench_obj": None,
            "elapsed_s": elapsed,
            "why": f"exit {proc.returncode}",
            "stderr_tail": tail,
        }
    match mode:
        case "judge":
            try:
                payload = json.loads(proc.stdout)
            except json.JSONDecodeError:
                return {
                    "name": name,
                    "alive": False,
                    "by_file": {},
                    "bench_obj": None,
                    "elapsed_s": elapsed,
                    "why": "stdout is not a JSON array",
                    "stderr_tail": tail,
                }
            if not isinstance(payload, list):
                return {
                    "name": name,
                    "alive": False,
                    "by_file": {},
                    "bench_obj": None,
                    "elapsed_s": elapsed,
                    "why": "stdout is not a JSON array",
                    "stderr_tail": tail,
                }
            by_file = _index_rows(payload)
            if n_judge_files >= 1 and not by_file:
                return {
                    "name": name,
                    "alive": False,
                    "by_file": {},
                    "bench_obj": None,
                    "elapsed_s": elapsed,
                    "why": "0 rows",
                    "stderr_tail": tail,
                }
            return {
                "name": name,
                "alive": True,
                "by_file": by_file,
                "bench_obj": None,
                "elapsed_s": elapsed,
                "why": "",
                "stderr_tail": tail,
            }
        case "bench":
            assert tmp is not None
            path = tmp / f"{name}.json"
            try:
                text = path.read_text(encoding="utf-8")
                payload = json.loads(text)
            except (OSError, json.JSONDecodeError):
                return {
                    "name": name,
                    "alive": False,
                    "by_file": {},
                    "bench_obj": None,
                    "elapsed_s": elapsed,
                    "why": "results file missing or not a BAYBENCH document",
                    "stderr_tail": tail,
                }
            if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
                return {
                    "name": name,
                    "alive": False,
                    "by_file": {},
                    "bench_obj": None,
                    "elapsed_s": elapsed,
                    "why": "results file missing or not a BAYBENCH document",
                    "stderr_tail": tail,
                }
            return {
                "name": name,
                "alive": True,
                "by_file": _index_rows(payload["results"]),
                "bench_obj": payload,
                "elapsed_s": elapsed,
                "why": "",
                "stderr_tail": tail,
            }
        case _ as unreachable:
            raise AssertionError(f"unreachable mode: {unreachable!r}")


def run_engines(
    input_dir: Path,
    *,
    engines: list[str],
    budget_s: float | None,
    detector_budget_s: float,
    python: str,
    node: str,
    mode: str,
    n_judge_files: int,
) -> dict[str, dict]:
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    tmp: Path | None = None
    outcomes: dict[str, dict] = {}
    try:
        if mode == "bench":
            tmp = Path(tempfile.mkdtemp(prefix="ensemble-"))
        threads: list[threading.Thread] = []

        def worker(name: str) -> None:
            cmd = _engine_command(
                name, mode, input_dir, python, node, detector_budget_s, tmp
            )
            result = _run_one_engine(
                name,
                cmd,
                mode=mode,
                budget_s=budget_s,
                env=env,
                tmp=tmp,
                n_judge_files=n_judge_files,
            )
            outcomes[name] = result

        for name in engines:
            thread = threading.Thread(target=worker, args=(name,), daemon=True)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return outcomes
    finally:
        if tmp is not None:
            shutil.rmtree(tmp, ignore_errors=True)


def _emit_engine_logs(engines: list[str], outcomes: dict[str, dict]) -> None:
    for name in engines:
        result = outcomes.get(name)
        if result is None:
            continue
        tail = result.get("stderr_tail") or ""
        if tail:
            sys.stderr.write(tail)
            if not tail.endswith("\n"):
                sys.stderr.write("\n")
        if result.get("alive"):
            logger.info(
                "%s: %s rows in %.1fs",
                name,
                len(result.get("by_file") or {}),
                result.get("elapsed_s") or 0.0,
            )
        else:
            logger.info(
                "DEGRADED: %s produced 0 rows (%s)",
                name,
                result.get("why") or "0 rows",
            )


def _alive_map(outcomes: dict[str, dict], name: str, selected: list[str]) -> dict[str, dict] | None:
    if name not in selected:
        return None
    result = outcomes.get(name)
    if result is None or not result.get("alive"):
        return None
    return result.get("by_file") or {}


def merge_bench_document(
    detector_run: dict | None,
    noexit_run: dict | None,
) -> dict:
    d_alive = bool(detector_run and detector_run.get("alive"))
    n_alive = bool(noexit_run and noexit_run.get("alive"))
    if d_alive and not n_alive:
        assert detector_run is not None
        payload = detector_run.get("bench_obj") or {"results": []}
        results = payload.get("results") if isinstance(payload, dict) else []
        if not isinstance(results, list):
            results = []
        return {
            "tool": {"name": "ensemble", "version": _tool_version(payload if isinstance(payload, dict) else None)},
            "results": results,
        }
    if n_alive and not d_alive:
        assert noexit_run is not None
        payload = noexit_run.get("bench_obj") or {"results": []}
        results = payload.get("results") if isinstance(payload, dict) else []
        if not isinstance(results, list):
            results = []
        return {
            "tool": {"name": "ensemble", "version": _tool_version(payload if isinstance(payload, dict) else None)},
            "results": results,
        }
    if not d_alive and not n_alive:
        return {"tool": {"name": "ensemble", "version": "+"}, "results": []}
    assert detector_run is not None and noexit_run is not None
    d_map = detector_run.get("by_file") or {}
    n_map = noexit_run.get("by_file") or {}
    names = list(d_map)
    for key in n_map:
        if key not in d_map:
            names.append(key)
    names.sort()
    results = [merge_bench(name, d_map.get(name), n_map.get(name)) for name in names]
    d_ver = _tool_version(detector_run.get("bench_obj"))
    n_ver = _tool_version(noexit_run.get("bench_obj"))
    return {
        "tool": {"name": "ensemble", "version": f"{d_ver}+{n_ver}"},
        "results": results,
    }


def _write_judge(rows: list[dict]) -> None:
    sys.stdout.write(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")


def _parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="ensemble.py")
    parser.add_argument("input_dir", nargs="?", type=Path)
    parser.add_argument("--bench-out", type=Path, default=None)
    parser.add_argument("--budget", type=float, default=None)
    parser.add_argument("--engines", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _configure_logging()
    raw = list(sys.argv[1:] if argv is None else argv)
    try:
        args = _parse_cli(raw)
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 2
        if code == 0:
            return 0
        _write_judge([])
        return 2

    env_engines = os.environ.get("ENSEMBLE_ENGINES")
    env_budget = os.environ.get("ENSEMBLE_BUDGET_S")
    env_detector_budget = os.environ.get("ENSEMBLE_DETECTOR_BUDGET_S")
    env_python = os.environ.get("ENSEMBLE_PYTHON")
    env_node = os.environ.get("ENSEMBLE_NODE")
    env_mode = os.environ.get("ENSEMBLE_MODE")

    if args.input_dir is None or not args.input_dir.is_dir():
        sys.stderr.write(
            "usage: ensemble.py <dir> [--bench-out PATH] [--budget S] "
            "[--engines detector,noexit]\n"
        )
        _write_judge([])
        return 2

    input_dir = args.input_dir
    engines_raw = args.engines if args.engines is not None else (env_engines or "")
    engines = parse_engines(engines_raw) if engines_raw.strip() else ["detector", "noexit"]
    if env_detector_budget not in (None, ""):
        detector_budget_s = float(env_detector_budget)
    else:
        detector_budget_s = 420.0
    python = env_python if env_python else sys.executable
    node = env_node if env_node else "node"

    if args.bench_out is not None:
        mode = "bench"
        bench_out = args.bench_out
    else:
        raw_mode = (env_mode or "").strip().lower()
        match raw_mode:
            case "judge" | "bench":
                mode = raw_mode
            case "":
                mode = _auto_mode()
            case _:
                logger.warning(
                    "unknown ENSEMBLE_MODE=%r; falling back to auto-detect", env_mode
                )
                mode = _auto_mode()
        bench_out = Path("/output/results.json") if mode == "bench" else None

    budget_s = effective_budget(mode, args.budget, env_budget)
    judge_files = list_judge_files(input_dir) if mode == "judge" else []
    files_label: str = str(len(judge_files)) if mode == "judge" else "n/a"
    t0 = time.monotonic()
    budget_label = "none" if budget_s is None else f"{budget_s}s"
    logger.info(
        "engines=%s budget=%s detector_budget=%ss mode=%s files=%s",
        engines,
        budget_label,
        detector_budget_s,
        mode,
        files_label,
    )

    rows: list[dict] | None = None
    try:
        outcomes = run_engines(
            input_dir,
            engines=engines,
            budget_s=budget_s,
            detector_budget_s=detector_budget_s,
            python=python,
            node=node,
            mode=mode,
            n_judge_files=len(judge_files),
        )
        _emit_engine_logs(engines, outcomes)
        match mode:
            case "judge":
                d_map = _alive_map(outcomes, "detector", engines)
                n_map = _alive_map(outcomes, "noexit", engines)
                rows = merge_all(judge_files, d_map, n_map)
                elapsed = time.monotonic() - t0
                n_mal = sum(1 for row in rows if row["verdict"] == "MALICIOUS")
                n_ben = sum(1 for row in rows if row["verdict"] == "BENIGN")
                n_unc = sum(1 for row in rows if row["verdict"] == "UNCERTAIN")
                logger.info(
                    "%s files -> %s MALICIOUS / %s BENIGN / %s UNCERTAIN in %.1fs",
                    len(rows),
                    n_mal,
                    n_ben,
                    n_unc,
                    elapsed,
                )
                _write_judge(rows)
                return 0
            case "bench":
                assert bench_out is not None
                d_run = outcomes.get("detector") if "detector" in engines else None
                n_run = outcomes.get("noexit") if "noexit" in engines else None
                document = merge_bench_document(d_run, n_run)
                bench_out.write_text(
                    json.dumps(document, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                logger.info(
                    "%s files -> results.json written to %s",
                    len(document.get("results") or []),
                    bench_out,
                )
                return 0
            case _ as unreachable:
                raise AssertionError(f"unreachable mode: {unreachable!r}")
    except Exception:
        logger.exception("ensemble failed")
        if mode == "judge":
            _write_judge(rows if rows is not None else [])
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
