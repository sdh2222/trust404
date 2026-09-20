# Track 1 Ensemble — Spec

Two-engine merge entry point for TRUST404 Track 1. Detector (Python / Slither) and noexit (TypeScript AST) are complete tools on their own; this document is the SSOT for how `tools/ensemble.py` and `run.sh` combine them. Bench contract from [baybench.md](baybench.md); judge schema from `detector/schema/judge.schema.json`.

## Purpose

One directory in, one judge array (or one BAYBENCH `results.json`) out, with both engines asked the same question. An "either-MALICIOUS" merge beats consensus because the engines never accuse a labelled-benign file: on the 673 compiling files, consensus scores 0.869, detector alone 0.923, and either-MALICIOUS 0.941. The BENIGN rule is asymmetric — only detector's BENIGN counts — because noexit said BENIGN on 33 malicious files detector flagged or could not compile; that rule scores 0.752 vs 0.745 (symmetric BENIGN) on all 862 labelled files (20 vs 26 wrong). The corpus has no non-compiling benign file, so the cost side of the asymmetric BENIGN rule is unmeasured.

## Engines and commands

Selected engines run concurrently (`threads` + `subprocess.run`, `cwd` = repo root, `PYTHONPATH` = repo root). Judge form walks top-level `*.sol` only (`file` = basename). Bench form is recursive (`file` = path relative to `<dir>`).

- **detector judge:** `<python> -m detector.cli <dir> --budget <ENSEMBLE_DETECTOR_BUDGET_S>`
- **noexit judge:** `node noexit/dist/cli.js judge <dir>`
- **detector bench:** `<python> -m detector.cli <dir> <tmp>/detector.json --no-summary`
- **noexit bench:** `node noexit/dist/baybench.js <dir> <tmp>/noexit.json`

CLI: `python tools/ensemble.py <dir> [--bench-out PATH] [--budget S] [--engines detector,noexit]`.

## Verdict rule

`decide(d, n)` over uppercase verdicts. `None` means the engine is alive but produced no row for this file (a dead engine is handled by the fallback in [Engine failure and DEGRADED](#engine-failure-and-degraded), not by this table). Unknown strings normalise to `UNCERTAIN`. M = MALICIOUS, B = BENIGN, U/None = UNCERTAIN or missing row.

| d \ n | M | B | U/None |
|---|---|---|---|
| M | M | M | M |
| B | M | B | B |
| U/None | M | U | U |

- `MALICIOUS` if either engine says `MALICIOUS`.
- else `BENIGN` if detector says `BENIGN`.
- else `UNCERTAIN`.

Judge merge (both engines alive): voters are the engines whose normalised verdict equals the final (detector first). `reasons` / `evidence` are the ordered union over voters (non-empty strings / cleaned `{function, line}` items; dict-equality dedupe). For `UNCERTAIN`, `reasons` is the union over both rows so a compile-failure note is kept. `MALICIOUS` with empty evidence is downgraded to `UNCERTAIN`. Bench merge: Title-case of `decide`; findings = detector's then noexit's not already present; `reason` only when the final is `Uncertain`.

## Engine failure and DEGRADED

An engine is **alive** iff it finished within the budget, parsed as the expected JSON shape, and (judge mode, input has ≥ 1 top-level `.sol`) produced ≥ 1 row. Otherwise stderr gets `DEGRADED: <engine> produced 0 rows (<why>)` with `why` ∈ {`timeout after Ns`, `exit <code>`, `stdout is not a JSON array`, `0 rows`}.

- Exactly one engine alive → that engine's rows, normalised; the merge rule is not applied.
- Both alive → per-file `decide` / merge above.
- None alive → every input file is `UNCERTAIN` with reason `Both engines failed or timed out; no verdict could be produced.`
- `run.sh` mirrors this: if exactly one wanted engine is available it exports `ENSEMBLE_ENGINES=<available>` and prints `DEGRADED`; if none are available it exits 2 with empty stdout.

## Modes and environment variables

`ENSEMBLE_MODE=judge|bench`; if unset, bench iff `/output` is a writable directory, else judge. `--bench-out PATH` forces bench mode with that path; auto-detected bench writes `/output/results.json`. Env is read once in `main` and passed down.

| Variable | Default | Role |
|---|---|---|
| `ENSEMBLE_ENGINES` | `detector,noexit` | Comma list; unknown names are ignored; empty after filtering → both. Overridden by `--engines`. |
| `ENSEMBLE_BUDGET_S` | `540` in judge mode, **none** in bench mode | Per-engine subprocess timeout in judge mode. In bench mode the wall clock is BAYBENCH's `bench run --timeout`, not the ensemble. `--budget` or the env var override both. |
| `ENSEMBLE_DETECTOR_BUDGET_S` | `420.0` | Passed to detector as `--budget` (`420 +` one 120 s file `= 540`). |
| `ENSEMBLE_PYTHON` | `sys.executable` | Interpreter used to launch detector. |
| `ENSEMBLE_NODE` | `node` | Node binary used to launch noexit. |
| `ENSEMBLE_MODE` | auto (`/output`) | `judge` or `bench`. |

## Determinism

Every output-affecting walk is over sorted keys or insertion-ordered lists. Judge stdout and bench `results.json` are `json.dumps(..., indent=2, ensure_ascii=False) + "\n"`. Two runs on the same input are byte-identical.

## Acceptance

| ID | Criterion | Status |
|---|---|---|
| EN-1 | judge output: `python tools/ensemble.py <dir>` prints one schema-valid array, one row per top-level `.sol`, logs on stderr, exit 0; empty dir → `[]` | met — `tests/ensemble/test_cli.py` |
| EN-2 | verdict rule: `decide` table exhaustively unit-tested; MALICIOUS without evidence downgrades | met — `tests/ensemble/test_merge.py` |
| EN-3 | degraded mode: a dead engine yields a `DEGRADED` stderr line and the surviving engine's verdicts; both dead → all UNCERTAIN; `run.sh` mirrors this and exits 2 only when no engine is available | met — `tests/ensemble/test_cli.py`, `tests/ensemble/test_merge.py`, `tests/detector/test_run_sh.py` |
| EN-4 | determinism: judge stdout and bench `results.json` byte-identical across two runs | met — `test_judge_mode_deterministic`, `test_bench_mode_deterministic` |
| EN-5 | bench parity: `bench run ensemble --repeat 2` (Docker, `--network none`, all tiers) determinism pass; Tier 0 5/5; Tier 1 and Tier 3 HIGH-FP 0; weighted score and every tier mean ≥ detector's **on labels that admit a decisive answer** — the 250 Tier 2 `non-compiling paper fixture` labels stay Uncertain-only by owner decision (2026-09-20), so Tier 2 is compared on the 529 Malicious-labelled files (Malicious / Benign-miss / Uncertain counts) | owner amend 2026-09-20 (Henry); rescoring pending — orchestrator fills from `reports/ensemble/` and `reports/detector/` after the label amend (Run 9) |
| EN-6 | image: `trust404/ensemble` runs as any uid, on a read-only rootfs, with `--network none`, both engines alive (no `DEGRADED`) | met (local arm64 build trust404/ensemble:wip-c) — tests/detector/test_docker_hardening.py ensemble rows: root / uid 1000 / uid 65534 read-only cap-drop 2 vCPU 4 GB / read-only no tmpfs / ENSEMBLE_MODE=judge with /output mounted, both engines alive, stdout cmp-identical; amd64 digest pending submission-rc2 |
