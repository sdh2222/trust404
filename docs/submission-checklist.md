# Submission checklist (owner)

State as of 2026-09-20 22:30 KST. Everything is done and merged; owner actions 1 and 2 were completed 2026-09-20 (package public, repo public; anonymous manifest inspect of both digests and the release tarball verified). Only step 3, the form itself, remains.

## What is shipped

| item | value |
|---|---|
| tag / commit | `submission-rc2` = `3474ffc` (`main` tip `9ced656` differs only by this README/digest fill) |
| ensemble image (judges run this) | `ghcr.io/sdh2222/trust404-ensemble@sha256:0822a5a91630f53a1f4acf86ff97ecf5c83be5648361c4e1967ca6dde3a47440` (`:submission-rc2`, `:latest`; `linux/amd64`) |
| detector image (base of the ensemble) | `ghcr.io/sdh2222/trust404-detector@sha256:5de570d30a3636712fb9b8ee10f23cfc9aaa80ba81da2c3669fb178f89d9363f` |
| release | https://github.com/sdh2222/trust404/releases/tag/submission-rc2 — `trust404-ensemble-amd64.tar.gz` sha256 `8daa316f7a81ec5f8346a732710bb7c1fcdb06d5fbcd3d4a5db69a609fa54eac` (454 MB), `trust404-detector-amd64.tar.gz` sha256 `777ddac8989d53bc7bdeb35a73e29f2740a5f7ea7e5c6a56d79c3ae303aebb61` (322 MB) |
| gate on `3474ffc` | `pytest` 1098 passed incl. `DETECTOR_DOCKER_TESTS=1` (14 hardening rows); `bench run detector --repeat 2` determinism pass |
| bench (Run 9, all tiers, Docker, BAYBENCH weighted) | ensemble **0.9803**, detector 0.9703; Tier 0 5/5 both; ensemble Tier 1 1.0, Tier 3 1.0; 0 HIGH-FP on Tier 1/3 (`docs/bench/misses.md` Run 9) |
| verified by digest | ensemble digest pulled by hash, run `--network none --user 65534:65534 --read-only --tmpfs /tmp --cap-drop ALL --security-opt no-new-privileges --memory 4g --cpus 2 --pids-limit 512` on the five public samples: P1/P4 BENIGN, P2/P3/P5 MALICIOUS, both engines alive, schema-valid |

## Owner actions (in this order)

1. ~~Make the ensemble package public~~ — done 2026-09-20 (`gh api /user/packages/container/trust404-ensemble` → `visibility: public`; anonymous `docker manifest inspect` of both digests OK).
2. ~~Decide repo visibility~~ — done 2026-09-20: repo is public (`gh repo edit --visibility public`); release tarball URL answers 200 anonymously.
3. **Submit.** Paste, in this form:
   - image: `ghcr.io/sdh2222/trust404-ensemble@sha256:0822a5a91630f53a1f4acf86ff97ecf5c83be5648361c4e1967ca6dde3a47440`
   - run: `docker run --rm --network none -v "$PWD/input":/input:ro ghcr.io/sdh2222/trust404-ensemble@sha256:0822a5a91630f53a1f4acf86ff97ecf5c83be5648361c4e1967ca6dde3a47440 > out.json` (arm64 hosts add `--platform linux/amd64`)
   - repo + tag: https://github.com/sdh2222/trust404 @ `submission-rc2` (`3474ffc`); entry point `./run.sh <dir>`
   - fallback: release tarball + sha256 above, `docker load < trust404-ensemble-amd64.tar.gz`

## Verify after the clicks (30 seconds)

```bash
docker logout ghcr.io
docker manifest inspect ghcr.io/sdh2222/trust404-ensemble@sha256:0822a5a91630f53a1f4acf86ff97ecf5c83be5648361c4e1967ca6dde3a47440 >/dev/null && echo "anonymous pull OK"
mkdir -p in && cp cases/tier0_judge/*/*.sol in/
docker run --rm --platform linux/amd64 --network none --read-only --tmpfs /tmp --user 65534:65534 \
  -v "$PWD/in":/input:ro ghcr.io/sdh2222/trust404-ensemble@sha256:0822a5a91630f53a1f4acf86ff97ecf5c83be5648361c4e1967ca6dde3a47440 > out.json
python -m detector.submission --validate out.json   # expect P1/P4 BENIGN, P2/P3/P5 MALICIOUS
```

## If something must change after rc2 (cutting rc3)

1. Land the change through a PR (branch protection; `ci` green). No engine change → images are cache-identical, but the tag rule still applies.
2. On the exact `main` tip: `DETECTOR_DOCKER_TESTS=1 pytest tests -q -p no:cacheprovider` and `bench run detector --repeat 2` (never concurrent with another `bench run`).
3. `git tag -a submission-rc3 <tip> -m "..." && git push origin submission-rc3` — `detector-image.yml` builds both amd64 images, runs both hardened smoke matrices, pushes `:submission-rc3` + `:latest`, creates the release with both tarballs.
4. Read the digests from the run's job summary, fill them into `README.md` (*Get the runtime* and *Single-engine images*) via a PR, and re-run the verify block above with the new digest.

## Not done (known, not blocking)

- ~~Merge rule, Benign vote~~ — issue #8 measured and closed 2026-09-20: on the vendored noexit build the Benign-veto rule is identical to the shipped rule on every file (noexit never says Uncertain where detector says Benign); symmetric Benign is worse (0.747 vs 0.754, +6 wrong); consensus 0.681. Table on the issue and in `README.md`.
- ~~README organizers' +1/0/−1 table~~ — re-derived 2026-09-20 on `submission-rc2` (detector Run 9 + `bench run noexit --no-docker --repeat 2` on the vendored build): ensemble 0.754 / 0.944, detector 0.723 / 0.926, noexit 0.672 / 0.847. Metric definition is now written under the table.
- **Detector Tier 2 backlog** (`docs/bench/misses.md`, rows marked open): 16 Benign-miss on Malicious-labelled files that the ensemble does not recover, and one reasons-quality row (`BAL_PRIV_MINT` listed on OZ v5 `seize` probes). Recall work, post-deadline.
- **Hojae** (asked on #1): push T404 so `noexit/UPSTREAM` names a reachable commit. Checked 2026-09-20 22:05: `ghwo336/T404` master is still `332aae9`; `cbcef71a` is not on it. The vendored copy here is complete and self-contained, so this is provenance, not a blocker; since this repo is now public the "settle the fork" question is moot.
- noexit `determinism` shows `fail` in `reports/noexit/report.md` although verdicts are identical across repeats: its `reason` string embeds the absolute staging path (`.bench_work/noexit/runN/…`), which differs per run. noexit-side fix (upstream T404) or a bench-side path normalisation; cosmetic.
- Another session's working-tree files (`docs/research/**`, `reports/baseline_*`, `tools/baseline_slither/tool.py`, `chartkit.py`, `public set/`) are uncommitted and untouched by this plan.
