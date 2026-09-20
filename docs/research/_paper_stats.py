#!/usr/bin/env python3
"""Derived statistics for the academic paper.

Reads the labelled corpus under `cases/` and the committed per-case rows in
`reports/<tool>/report.json` (`scoring.cases`), and prints every derived number
the paper cites that is not already a summary field of that report: verdict
confusion matrices, the Tier 2 compiling-malicious split, and the family
attribution distribution.

Both inputs are committed, so the output is reproducible from a checkout of the
commit the paper reports; the raw `results.json` files under `.bench_work/` are
local run artifacts and are not required. Nothing here scores; scoring stays in
`baybench.scoring`.

The corpus and the reports keep moving. This script checks each report against
the paper's snapshot and warns when one has been re-run on a different corpus,
so a drifted number is never printed as if the paper used it.

Run from the repo root:

    .venv/bin/python docs/research/_paper_stats.py

To reproduce the paper's own numbers once the working tree has moved on:

    git stash && git checkout 799361b -- reports cases   # or read them with git show
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from baybench.models import load_cases  # noqa: E402

# The paper reports the frozen 859-case run at commit 799361b. The working tree
# moves on, so say so loudly rather than printing numbers the paper does not use.
SNAPSHOT, SNAPSHOT_N = "799361b", 859

TOOLS = ("detector", "noexit", "baseline_slither", "baseline_keyword")
VERDICTS = ("Benign", "Malicious", "Uncertain")
TIERS = ("tier0_judge", "tier1_pairs", "tier2_realworld", "tier3_benign_risky")


def report(tool: str) -> dict:
    return json.loads((ROOT / "reports" / tool / "report.json").read_text())


def main() -> None:
    cases = load_cases(ROOT / "cases")
    by_id = {case.id: case for case in cases}

    drift = []
    for tool in TOOLS:
        scoring = report(tool)["scoring"]
        n = len(scoring["cases"])
        flag = "" if n == SNAPSHOT_N else f"  <-- NOT the paper's snapshot ({SNAPSHOT_N})"
        if flag:
            drift.append(tool)
        print(f"== {tool}: weighted {scoring['weighted_score']}, {n} case rows{flag}")
    if drift:
        print(f"\nWARNING: {', '.join(drift)} have been re-run on a different corpus since "
              f"commit {SNAPSHOT}.\n         The paper's derived numbers below no longer come "
              f"from the run it reports.\n         Read them from that commit instead:  "
              f"git show {SNAPSHOT}:reports/<tool>/report.json")

    rows = report("detector")["scoring"]["cases"]
    by_case = {row["id"]: row for row in rows}

    print("\n== detector verdict confusion (rows = preferred label, cols = verdict)")
    print(f"{'tier':<20}{'label':<11}" + "".join(f"{v:>11}" for v in VERDICTS))
    for tier in TIERS:
        tier_rows = [row for row in rows if row["tier"] == tier]
        grid: Counter = Counter()
        for row in tier_rows:
            grid[(row["preferred"], row["actual"] or "missing")] += 1
        present = {row["preferred"] for row in tier_rows}
        for label in VERDICTS:
            if label not in present:
                continue
            counts = [grid[(label, v)] for v in VERDICTS]
            print(f"{tier:<20}{label:<11}" + "".join(f"{n:>11}" for n in counts))

    print("\n== Tier 2, Malicious-labelled files, split by whether the file compiled")
    compiled: Counter = Counter()
    failed = 0
    for row in rows:
        if row["tier"] != "tier2_realworld" or row["preferred"] != "Malicious":
            continue
        if row["compile_fail"] or row["actual"] is None:
            failed += 1
        else:
            compiled[row["actual"]] += 1
    total = sum(compiled.values()) + failed
    print(f"Malicious-labelled: {total}; compile_failed: {failed}; "
          f"compiling: {sum(compiled.values())} -> {dict(compiled)}")

    print("\n== family attribution on labelled-malice cases (preferred Malicious, "
          "expected_families non-empty)")
    labelled = [
        case for case in cases
        if case.preferred_verdict == "Malicious" and case.expected_families
    ]
    fired_counts = []
    extras = []
    three_plus = 0
    three_plus_malicious = 0
    for case in labelled:
        row = by_case.get(case.id, {})
        fams = set(row.get("fired_families") or ())
        fired_counts.append(len(fams))
        extras.append(len(fams - set(case.expected_families)))
        if len(fams) >= 3:
            three_plus += 1
            if row.get("actual") == "Malicious":
                three_plus_malicious += 1
    n = len(labelled)
    print(f"labelled-malice cases: {n}")
    print(f"single-tag labels: {sum(1 for c in labelled if len(c.expected_families) == 1)}")
    print(f"cases firing 3+ families: {three_plus} ({three_plus / n:.1%}); "
          f"of those, still Malicious: {three_plus_malicious}")
    print(f"mean families fired: {sum(fired_counts) / n:.2f}; "
          f"mean extra (not in the label): {sum(extras) / n:.2f}")

    print("\n== corpus composition")
    for tier in TIERS:
        tier_cases = [c for c in cases if c.tier == tier]
        labels = Counter(c.preferred_verdict for c in tier_cases)
        print(f"{tier:<20} n={len(tier_cases):<5} {dict(labels)}")
    t2 = [c for c in cases if c.tier == "tier2_realworld"]
    print("tier2 by source:", dict(Counter(c.id.split("/")[1] for c in t2)))
    pied = [c for c in t2 if c.id.split("/")[1] == "pied-piper"]
    print("pied-piper by kind:", dict(Counter(c.id.split("/")[2].split("_")[0] for c in pied)))
    print("honeybadger by technique:", dict(Counter(
        (c.source or "").split(": ", 1)[-1]
        for c in t2 if c.id.split("/")[1] == "honeybadger"
    )))
    print("crpwarner by manifest note:", dict(Counter(
        (c.source or "").split(": ", 1)[-1] or "(none)"
        for c in t2 if c.id.split("/")[1] == "crpwarner"
    )))

    print("\n== HIGH False Positive denominator")
    benign = [c for c in cases if c.preferred_verdict == "Benign"]
    print(f"Benign-preferred cases: {len(benign)} "
          f"(tier0 {sum(1 for c in benign if c.tier == 'tier0_judge')}, "
          f"tier1 {sum(1 for c in benign if c.tier == 'tier1_pairs')}, "
          f"tier3 {sum(1 for c in benign if c.tier == 'tier3_benign_risky')})")
    _ = by_id


if __name__ == "__main__":
    main()
