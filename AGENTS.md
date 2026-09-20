# Agent brief

This is the TRUST404 Track 1 submission: an ensemble of `detector/` (ours, Python ≥ 3.11, Slither IR) and `noexit/` (Hojae's, TypeScript AST). BAYBENCH scores both engines. The judge entry point is `run.sh` / the trust404/ensemble image, which prints one JSON array on stdout.

## Layout / ownership

From `CONTRIBUTING.md`:

| path | owner |
|---|---|
| `detector/` | ours (Python, Slither IR) |
| `noexit/` | vendored from ghwo336/T404; never edited here (`noexit/UPSTREAM`) |
| `tools/ensemble.py`, `run.sh`, root Dockerfile | shared: propose, do not land alone |
| `baybench/`, `cases/`, `docs/specs/`, `docs/bench/misses.md` | bench, labels, specs, triage |

## Setup

- Local: `scripts/setup_local.sh` (Python ≥ 3.11; Node ≥ 18; 46 solc binaries; builds noexit when node/npm are present).
- Docker (both images):
  - `docker build -f detector/Dockerfile -t trust404/detector:latest .`
  - `docker build --build-arg BASE=trust404/detector:latest -t trust404/ensemble:latest .`

## Verify a change

- `pytest tests -q -p no:cacheprovider`
- `bench validate`
- `JUDGE_SMOKE_REQUIRE_ENGINES=detector,noexit scripts/judge_smoke.sh <dir>`
- `./run.sh <dir> > out.json && python -m detector.submission --validate out.json`
- When images changed: `DETECTOR_DOCKER_TESTS=1 pytest tests/detector/test_docker_hardening.py`

## Bench rules

- Never run two `bench run` at once (they share `.bench_work/`).
- Quote a number only with tool, commit, tier set, and metric (organizers' +1/0/−1 vs BAYBENCH weighted).
- A Tier 0 verdict moving off the organizers' label is a stop.
- A Tier 1/3 label change needs a labels.yaml amendment and a `docs/bench/misses.md` row in the same PR.

## Judge-run invariants

From `CONTRIBUTING.md` and `docs/specs/detector.md`:

- one JSON array on stdout; everything else on stderr
- offline after ENTRYPOINT
- any uid; read-only rootfs
- solc set from `detector/solc_versions.txt`; OpenZeppelin v4 and v5 vendored
- default judge budget is 540 s (`ENSEMBLE_BUDGET_S` in `docs/specs/ensemble.md` / `tools/ensemble.py`); detector `--budget` is 420 s plus one 120 s file. Files past the budget are emitted as UNCERTAIN, never dropped.

## Do-not

- edit `noexit/**` in this repo
- change a label without a `docs/bench/misses.md` row
- push `main`
- `git add -A`
- use the network after ENTRYPOINT
- run two concurrent `bench run`
- commit another session's files

## Pointers

- `docs/specs/detector.md`
- `docs/specs/baybench.md`
- `docs/specs/ensemble.md`
- `CONTRIBUTING.md`
- `docs/agents/grok-subagent-guardrails.md`
- `docs/bench/misses.md`
