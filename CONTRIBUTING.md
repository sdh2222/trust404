# Working in this repo (team + agents)

Two engines, one bench, one entry point. This page is the contract between the people and the
agents that touch `trust404` and `T404`.

## What lives where

| path | owner | what it is |
|---|---|---|
| `detector/` | trust404 (`sdh2222`) | Python detector on Slither IR. Spec: `docs/specs/detector.md`. |
| `noexit/` (once merged) | T404 (Hojae, `ghwo336`) | TypeScript AST detector, vendored from `github.com/ghwo336/T404`. Upstream commit in `noexit/UPSTREAM`. |
| `tools/ensemble.py`, `run.sh`, root `Dockerfile` | shared | judges' entry point. Changes need both of us on the PR. |
| `baybench/`, `cases/`, `reports/` | shared | the bench. Labels and scoring are the SSOT for "better"; see below. |
| `docs/specs/*.md` | shared | acceptance tables. Rows are never deleted or renumbered; status moves OPEN → met with evidence. |

## Branch rules (enforced on `main`)

- No direct pushes. Every change is a PR, including from the repo owner and from agents.
- CI (`ci` workflow: pytest, `bench validate` on Tiers 0/1/3, judge smoke on the public set) must be green.
- One topic per PR. `noexit/` import, ensemble entry point, a detector rule fix, a label amendment
  — each is its own PR. A 130-file PR is not reviewable in a hackathon day.
- Squash-merge. The PR title becomes the commit; write it as the one-line changelog.
- No force-push to `main`, no branch deletion of `main`.

## Verdict changes are label changes

`cases/**/labels.yaml`, `baybench/scoring.py`, `detector/policy.py`, `detector/rules/**`,
`noexit/src/rules*.ts`: a PR that changes any Tier 0/1/3 verdict must

1. say which cases moved and in which direction,
2. cite the organizers' rule (`docs/judge/challenge_public/README.md`) or the spec row that justifies it,
3. add one row per moved verdict to `docs/bench/misses.md`,
4. attach the `bench run <tool> --repeat 2` summary line from the PR branch.

A Tier 0 verdict moving away from the organizers' label blocks the PR.

## How to run each tool on the bench

```bash
scripts/setup_local.sh                     # venv + the 46 pinned solc binaries
bench validate                             # every fixture compiles (or is labelled non-compiling)

bench run detector --no-docker             # ours, local venv
bench run detector                         # ours, Docker (trust404/detector:latest)

(cd noexit && npm ci --ignore-scripts && npx tsc -p tsconfig.json)   # build Hojae's engine once
bench run noexit --no-docker               # his, via noexit/dist/baybench.js

bench run ensemble                         # both merged (after the ensemble PR lands)
```

Reports land in `reports/<tool>/report.{md,json}`; commit them with the PR that changed the
number. Never run two `bench run` at once — they share `.bench_work/` and corrupt each other.

Running our detector from the T404 side or on a cold machine:

```bash
docker pull --platform linux/amd64 ghcr.io/sdh2222/trust404-detector:latest
./run.sh <dir> > out.json                  # picks Docker if the image is present, else the venv
scripts/judge_smoke.sh <dir>               # same as the judges: array on stdout, schema-checked
```

## Numbers you may quote

Only numbers produced by `bench run` on the corpus in this repo, with the tool name, the tree
(commit), and the tier set. "0.947 on 607 compiling cases" is fine if the report is committed;
otherwise it is an anecdote. The organizers' scale is +1 / 0 / −1 per file; BAYBENCH's weighted
score is ours — say which one you mean.

## Judge-run invariants (do not regress)

Anything under `run.sh`, `tools/ensemble.py`, `detector/Dockerfile`, root `Dockerfile` keeps:

- one JSON array on stdout, logs on stderr, exit 0 even when files fail;
- no network after `ENTRYPOINT`; solc pins from `detector/solc_versions.txt`; OZ v4 **and** v5 vendored;
- runs as any uid and on a read-only rootfs (`tests/detector/test_docker_hardening.py`, `DETECTOR_DOCKER_TESTS=1`);
- global budget under the organizers' 10 min, files past the budget emitted as `UNCERTAIN`, never dropped;
- `linux/amd64` image published by `detector-image.yml` on `submission-*` tags; the digest in the root README is what judges pull.

## Agents

Agents follow `.cursor/rules/team-workflow.mdc` in this repo (branch/PR rules above, no `main`
pushes, bench numbers before claims) and, for implementation subagents,
`docs/agents/grok-subagent-guardrails.md`.
Repo brief for any coding agent: `AGENTS.md`.
