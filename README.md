# BAYBENCH

Coding agents: see [AGENTS.md](AGENTS.md).

## TRUST404 Track 1 submission — judges start here

Two independent offline engines (detector: Python on Slither IR, privilege → state → transfer-path reasoning; noexit: TypeScript AST rules, tolerant parser) behind one entry point. Per file **MALICIOUS if either engine says so, BENIGN only when detector says so, UNCERTAIN otherwise**. stdout is exactly one JSON array; logs go to stderr. Consensus was measured and rejected (0.869 vs 0.941 on the compiling BAYBENCH subset) because the engines never disagree by accusing a benign file; see [`docs/specs/ensemble.md`](docs/specs/ensemble.md).

| | organizers' +1/0/−1, 862 labelled | compiling subset (673) | benign FP |
| --- | --- | --- | --- |
| detector | 0.720 | 0.923 | 0 |
| noexit | 0.669 | 0.844 | 0 |
| **ensemble** | **0.752** | **0.941** | **0** |

Caveat: the corpus has no non-compiling benign file, so the cost side of "BENIGN only from detector" is unmeasured.

### Prerequisites

- **Docker-only path** (what judges use): Docker 24+ (any engine that runs `docker run --network none --read-only`). Add `--platform linux/amd64` when the host is arm64 (the image is amd64 only). The ensemble image is ~2 GB on disk (`docker images`; the detector base is ~1.4 GB of that). The compressed pull size of the published amd64 image is listed next to its digest under *Get the runtime* once `submission-rc2` is tagged. Nothing else is needed on the host.
- **Local path** (no Docker): Python ≥ 3.11 (`requires-python = ">=3.11"` in `pyproject.toml`); `uv` optional. Node ≥ 18 (`engines.node` in `noexit/package.json`). npm. The 46 solc binaries listed in `detector/solc_versions.txt`, installed by `scripts/setup_local.sh` (which also builds noexit). Then `./run.sh <dir>`.
- **Validation only**: `python -m detector.submission --validate out.json` (offline, no solc needed) and optional `check-jsonschema`.
- **Network: when**
  - Downloads: `docker pull` / `docker load`; `scripts/setup_local.sh` (pip + solc binaries); `npm ci`.
  - Graded run: `./run.sh` / `docker run --network none` — none.
- **Sizes / times**: solc artifacts are 1.5G (`du -sh ~/.solc-select/artifacts`). First `scripts/setup_local.sh` run is ~10–15 min (46 solc downloads + pip + npm/tsc); re-runs skip installed compilers and existing `noexit/node_modules`.

### Get the runtime

1. Published `linux/amd64` ensemble image `ghcr.io/sdh2222/trust404-ensemble@sha256:<ENSEMBLE-DIGEST-TBD>` (also `:latest`), then `docker tag ghcr.io/sdh2222/trust404-ensemble@sha256:<ENSEMBLE-DIGEST-TBD> trust404/ensemble:latest`; or `docker load < trust404-ensemble-amd64.tar.gz` from the release (sha256 `<ENSEMBLE-SHA-TBD>`). Arm64 hosts add `--platform linux/amd64`.
2. `docker build --platform linux/amd64 --build-arg BASE=ghcr.io/sdh2222/trust404-detector:latest -t trust404/ensemble:latest .`
3. No Docker: `scripts/setup_local.sh && (cd noexit && npm ci --ignore-scripts && npx tsc -p tsconfig.json)` (Python ≥ 3.11, Node ≥ 18).

### Run

```bash
./run.sh ./cases > out.json
docker run --rm --network none -e ENSEMBLE_MODE=judge \
  -v "$PWD/cases":/input:ro trust404/ensemble:latest > out.json
```

`run.sh` prints the backend it chose on stderr; if one engine is unavailable it prints `run.sh: DEGRADED:` and runs the other; `ENSEMBLE_ENGINES=detector` (or `noexit`) forces a single engine.

### Validate

```bash
check-jsonschema --schemafile detector/schema/judge.schema.json out.json
JUDGE_SMOKE_REQUIRE_ENGINES=detector,noexit scripts/judge_smoke.sh ./cases
```

### Guarantees

- No network at runtime (both engines' dependencies are in the image).
- Works as any uid and on a read-only rootfs.
- Fits 2 vCPU / 4 GB / 10 min (ensemble budget 540 s: detector 420 s global + 120 s per file, noexit seconds; files past the budget are emitted as UNCERTAIN, never dropped).
- Exit 0 even when files or a whole engine fail (`[ensemble] DEGRADED:` on stderr).
- A MALICIOUS row always carries at least one code location.

### Single-engine images

- `docker pull ghcr.io/sdh2222/trust404-detector@sha256:947d696010cf61246793562dd708de1582cf732126b7714a74ef75b3540ca9dc` (also tagged `:submission-rc1`, `:latest`), then `docker tag ghcr.io/sdh2222/trust404-detector@sha256:947d696010cf61246793562dd708de1582cf732126b7714a74ef75b3540ca9dc trust404/detector:latest`
- or `docker load < trust404-detector-amd64.tar.gz` from the [release](https://github.com/sdh2222/trust404/releases/tag/submission-rc1) (sha256 `fc897f1fa13a73bf18726c840a6876fa253c1177f9dc1bc8a8fc9bdc19957393`)
- the manifest is `linux/amd64` only; on an arm64 host (Apple Silicon) add `--platform linux/amd64` to `docker pull` / `docker run` and it executes under qemu

```bash
docker run --rm --network none -e DETECTOR_MODE=submission \
  -v "$PWD/cases":/input:ro trust404/detector:latest > out.json
```

`noexit/run.sh <dir>` after building `noexit/dist`.

Verdict derivation: [detector/README.md](detector/README.md) · [noexit/README.md](noexit/README.md). Specs: [docs/specs/ensemble.md](docs/specs/ensemble.md), [docs/specs/detector.md](docs/specs/detector.md).

## BAYBENCH harness

Offline harness for TRUST404 Track 1 detectors. A tool is a black box: it reads a directory of `.sol` files and writes one `results.json`. BAYBENCH scores that output identically for every teammate, then lists the misses to iterate on. Pattern and rule IDs come from [docs/research/track1-malice-patterns.md](docs/research/track1-malice-patterns.md); the spec is [docs/specs/baybench.md](docs/specs/baybench.md).

## Install

```bash
uv venv --python 3.12 .venv && uv pip install -e '.[dev]'
```

## Commands

```bash
bench run baseline_keyword --tier 1 --no-docker
bench coverage --cases cases
bench coverage baseline_keyword --tier 1 --no-docker
bench validate --tier 1
bench report
bench ingest-discord path/to/discord-export
bench ingest-paper piedpiper path/to/sources
```

`bench run` double-runs by default (`--repeat 2`), writes `reports/<tool>/report.md` and `report.json`, and prints weighted score, determinism, and compile-fail count. `ingest-discord` / `ingest-paper` are seams for Tier 0 / Tier 2 (BB-8, BB-9); they exit 2 until those tasks land.

## `results.json` shape

```json
{
  "tool": {"name": "my_tool", "version": "0.1"},
  "results": [
    {
      "file": "tier1/EXIT_ADDR_GATE/mal/mal.sol",
      "verdict": "Malicious",
      "reason": "",
      "findings": [
        {
          "rule_id": "EXIT_ADDR_GATE",
          "family": "A",
          "severity": "HIGH",
          "contract": "Token",
          "function": "setBots",
          "lines": [41, 47],
          "reasoning": "hardcoded allowlist"
        }
      ]
    }
  ]
}
```

`file` is relative to the staged input root (`<case.id>/<case.file>`). Verdicts are `Benign | Malicious | Uncertain`. Schema: `baybench/schema/result.schema.json`.

## Register a tool

Add an entry to `baybench/tools.yaml`:

```yaml
tools:
  - name: baseline_keyword
    image: baybench/baseline_keyword:latest          # docker mode
  - name: my_local_tool
    cmd: "python /path/tool.py --in {input} --out {output}/results.json"  # --no-docker
  - name: noexit
    cmd: "node noexit/dist/baybench.js {input} {output}/results.json"  # vendored engine, build first
```

`{input}` and `{output}` are substituted in command mode. Docker mode mounts them at `/input` (ro) and `/output`. `cmd` is also env-expanded (for example `${MY_TOOL_DIR}`) with cwd = repo root; an unset variable is a clear error.

```bash
(cd noexit && npm ci --ignore-scripts && npx tsc -p tsconfig.json)
.venv/bin/bench run noexit --no-docker
```

## Grading parity

Grading parity is `docker run --rm --network none`. Network-dependent tools score zero by construction. The bench image (`Dockerfile.bench`) bakes in `solc-select` compilers so `bench validate` runs offline (BB-11):

```bash
docker build -f Dockerfile.bench -t baybench .
docker run --rm --network none baybench validate
```
