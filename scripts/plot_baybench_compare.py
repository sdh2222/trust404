from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import chartkit as ck  # noqa: E402
from baybench.catalog import load_catalog  # noqa: E402
from baybench.models import load_cases  # noqa: E402

OUT = ROOT / "reports"

# One color per tool, same on every chart.
TOOLS = (
    ("detector", "detector"),
    ("noexit", "noexit"),
    ("baseline_slither", "Slither"),
    ("baseline_keyword", "keyword"),
)
COLOR_BY_LABEL = {
    "detector": ck.C["blue"],
    "noexit": ck.C["green"],
    "Slither": ck.C["red"],
    "keyword": ck.C["purple"],
}
SOURCE = "BAYBENCH reports, EarthIsMine"
ASOF = "Sep 20, 2026"

FAMILY_NAME = {
    "A": "Exit gating",
    "B": "Balance tamper",
    "C": "Leak",
    "D": "Hidden owner",
    "E": "Structure",
    "F": "Honeypot / drain",
    "G": "Ponzi",
}
TIER_NAME = {
    "tier0_judge": "Tier 0",
    "tier1_pairs": "Tier 1",
    "tier2_realworld": "Tier 2",
    "tier3_benign_risky": "Tier 3",
}
TIER_GLOSS = (
    "Tier 0: organizers' public samples.  "
    "Tier 1: written twins per rule.  "
    "Tier 2: paper fixtures (injected and on-chain).  "
    "Tier 3: risky-looking benign."
)
RULE_LABEL = {
    "PRIV_ROLE": "privileged role",
    "EXIT_ADDR_GATE": "address gate",
    "EXIT_GLOBAL_SWITCH": "global switch",
    "EXIT_AMOUNT_LIMIT": "amount limit",
    "EXIT_TIME_GATE": "time gate",
    "EXIT_SELL_ONLY": "sell-only",
    "EXIT_CALLBACK_CYCLE": "callback cycle",
    "FEE_UNBOUNDED": "unbounded fee",
    "FEE_ADDR_MUTABLE": "mutable fee addr",
    "BAL_PRIV_MINT": "priv mint",
    "BAL_PRIV_BURN_OTHER": "burn-other",
    "BAL_DIRECT_SET": "direct set",
    "BAL_TRANSFER_HIDDEN_MINT": "hidden mint",
    "VIEW_CALLER_DEPENDENT": "caller-dep view",
    "LEAK_ARBITRARY_TRANSFERFROM": "arbitrary transferFrom",
    "LEAK_EXEMPT_PATH": "exempt path",
    "LEAK_PRIV_SWEEP": "priv sweep",
    "OWN_HIDDEN_ROLE": "hidden role",
    "OWN_FAKE_RENOUNCE": "fake renounce",
    "OWN_REASSIGN_NONSTD": "nonstd reassign",
    "OWN_TX_ORIGIN": "tx.origin",
    "STRUCT_EXTERNAL_GATE": "external gate",
    "STRUCT_DELEGATECALL_SETTABLE": "settable delegatecall",
    "STRUCT_SELFDESTRUCT": "selfdestruct",
    "STRUCT_PROXY_EOA_ADMIN": "proxy EOA admin",
    "DRAIN_APPROVAL_PULL": "approval pull",
    "HONEYPOT_LEGACY": "honeypot",
    "PONZI_SHAPE": "ponzi",
    "SLITHER_HIGH_OVERLAY": "Slither High",
}
T3_LABEL = {
    "tier3/bancor_smarttoken": "Bancor",
    "tier3/erc20_foreign_rescue": "foreign rescue",
    "tier3/lido_ldo_minime": "MiniMe / Lido",
    "tier3/oz_erc20_pausable_ownable": "OZ Pausable",
    "tier3/oz_erc20capped_accesscontrol": "OZ Capped",
    "tier3/oz_erc20permit": "OZ Permit",
    "tier3/reflection_token": "reflection",
    "tier3/usdc_fiattoken": "USDC",
}


def load_report(name: str) -> dict:
    return json.loads((OUT / name / "report.json").read_text())


def metric(rep: dict, section: str, keys: list[str], field: str) -> list[float]:
    return [rep["scoring"][section][key][field] for key in keys]


def scores(rep: dict, section: str, keys: list[str]) -> list[float]:
    return metric(rep, section, keys, "mean_verdict_score")


def series_for(reports: dict[str, dict], section: str, keys: list[str], field: str) -> dict[str, list[float]]:
    return {label: metric(reports[name], section, keys, field) for name, label in TOOLS}


def _label(ax, xpos: float, val: float, fontsize: float = 8) -> None:
    text = f"{val:.2f}"
    if val < 0.04:
        ax.text(xpos, 0.07, text, ha="center", va="bottom", fontsize=fontsize, color=ck.T["txt"])
    else:
        ax.text(xpos, val + 0.02, text, ha="center", va="bottom", fontsize=fontsize, color=ck.T["txt"])


def grouped_bars(
    ax,
    categories: list[str],
    series: dict[str, list[float]],
    fontsize: float = 8,
    rotate: float = 0,
) -> None:
    n = len(series)
    x = np.arange(len(categories))
    width = 0.78 / n
    offsets = (np.arange(n) - (n - 1) / 2) * width
    for i, (name, vals) in enumerate(series.items()):
        xs = x + offsets[i]
        ax.bar(xs, vals, width * 0.92, color=COLOR_BY_LABEL[name], label=name)
        for xpos, val in zip(xs, vals):
            _label(ax, float(xpos), val, fontsize=fontsize)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    if rotate:
        ck.rotate_xticks(ax, rotate)
    ax.set_ylim(0, 1.14)
    ck.pct_axis(ax, xmax=1, decimals=0)
    ck.legend(ax, loc="upper right", ncol=n)


def plot_weighted(reports: dict[str, dict]) -> None:
    names = [label for _, label in TOOLS]
    vals = [reports[name]["scoring"]["weighted_score"] for name, _ in TOOLS]
    colors = [COLOR_BY_LABEL[label] for label in names]
    fig, ax = ck.figure("publish", size="wide")
    bars = ax.bar(names, vals, width=0.55, color=colors)
    ax.set_ylim(0, 1.14)
    ck.pct_axis(ax, xmax=1, decimals=0)
    for bar, val in zip(bars, vals):
        _label(ax, bar.get_x() + bar.get_width() / 2, val, fontsize=11)
    ck.finish(
        fig,
        title="BAYBENCH weighted score by tool",
        source=SOURCE,
        asof=ASOF,
        brand="EarthIsMine",
        bottom_in=0.7,
        out=str(OUT / "baybench_weighted_score.png"),
    )


def _grouped(reports: dict[str, dict], title: str, out: str, categories: list[str],
             section: str, keys: list[str], field: str, size: str = "twitter",
             fontsize: float = 7.5, subtitle: str | None = None,
             bottom_in: float = 1.15) -> None:
    fig, ax = ck.figure("publish", size=size)
    grouped_bars(ax, categories, series_for(reports, section, keys, field), fontsize=fontsize)
    ck.finish(
        fig,
        title=title,
        subtitle=subtitle,
        source=SOURCE,
        asof=ASOF,
        brand="EarthIsMine",
        bottom_in=bottom_in,
        out=str(OUT / out),
    )


def _save(fig, title: str, out: str, subtitle: str | None = None, bottom_in: float = 0.7) -> None:
    ck.finish(
        fig,
        title=title,
        subtitle=subtitle,
        source=SOURCE,
        asof=ASOF,
        brand="EarthIsMine",
        bottom_in=bottom_in,
        out=str(OUT / out),
    )


def score_by_id(reports: dict[str, dict]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for name, label in TOOLS:
        out[label] = {row["id"]: row["score"] for row in reports[name]["scoring"]["cases"]}
    return out


def mean_score(ids: list[str], by_id: dict[str, float]) -> float:
    vals = [by_id[i] for i in ids if i in by_id]
    if not vals:
        raise ValueError(f"no scores for {ids}")
    return sum(vals) / len(vals)


def plot_from_series(title: str, out: str, categories: list[str],
                     series: dict[str, list[float]], size: str = "twitter",
                     fontsize: float = 7, rotate: float = 0,
                     subtitle: str | None = None, bottom_in: float = 1.15) -> None:
    fig, ax = ck.figure("publish", size=size)
    grouped_bars(ax, categories, series, fontsize=fontsize, rotate=rotate)
    _save(fig, title, out, subtitle=subtitle, bottom_in=bottom_in)


def plot_tier(reports: dict[str, dict]) -> None:
    keys = ["tier0_judge", "tier1_pairs", "tier2_realworld", "tier3_benign_risky"]
    _grouped(
        reports,
        "BAYBENCH mean verdict score by tier",
        "baybench_tier_named.png",
        [TIER_NAME[k] for k in keys],
        "per_tier",
        keys,
        "mean_verdict_score",
        subtitle=TIER_GLOSS,
        bottom_in=0.85,
    )


def plot_family(reports: dict[str, dict]) -> None:
    families = ["A", "B", "C", "D", "E", "F", "G"]
    labels = [FAMILY_NAME[f] for f in families]
    fig, ax = ck.figure("publish", size="twitter")
    grouped_bars(
        ax,
        labels,
        series_for(reports, "per_family", families, "mean_verdict_score"),
        fontsize=7,
    )
    _save(fig, "BAYBENCH mean verdict score by family", "baybench_family_named.png",
          bottom_in=0.85)


def plot_recall_tier(reports: dict[str, dict]) -> None:
    keys = ["tier1_pairs", "tier2_realworld"]
    _grouped(
        reports,
        "BAYBENCH family recall by tier",
        "baybench_recall_by_tier.png",
        [TIER_NAME[k] for k in keys],
        "per_tier",
        keys,
        "family_recall",
        size="wide",
        subtitle=TIER_GLOSS,
        bottom_in=0.85,
    )


def plot_recall_family(reports: dict[str, dict]) -> None:
    families = ["A", "B", "C", "D", "E", "F", "G"]
    labels = [FAMILY_NAME[f] for f in families]
    fig, ax = ck.figure("publish", size="twitter")
    grouped_bars(
        ax,
        labels,
        series_for(reports, "per_family", families, "family_recall"),
        fontsize=7,
    )
    _save(
        fig,
        "BAYBENCH family recall by family",
        "baybench_recall_by_family.png",
        bottom_in=1.35,
    )


def plot_tier_families(reports: dict[str, dict], cases) -> None:
    scores = score_by_id(reports)
    for tier, slug in (
        ("tier1_pairs", "tier1"),
        ("tier2_realworld", "tier2"),
    ):
        fams = []
        for fam in "ABCDEFG":
            ids = [
                c.id
                for c in cases
                if c.tier == tier and c.is_malicious and fam in c.expected_families
            ]
            if ids:
                fams.append((fam, ids))
        if not fams:
            continue
        categories = [FAMILY_NAME[f] for f, _ in fams]
        series = {
            label: [mean_score(ids, scores[label]) for _, ids in fams]
            for _, label in TOOLS
        }
        plot_from_series(
            f"BAYBENCH {TIER_NAME[tier]} mean verdict by family",
            f"baybench_score_{slug}_by_family.png",
            categories,
            series,
            bottom_in=1.35,
        )


def plot_tier3_lookalikes(reports: dict[str, dict], cases) -> None:
    scores = score_by_id(reports)
    rows = [c for c in cases if c.tier == "tier3_benign_risky"]
    categories = [T3_LABEL[c.id] for c in rows]
    ids = [c.id for c in rows]
    series = {label: [scores[label][i] for i in ids] for _, label in TOOLS}
    plot_from_series(
        f"BAYBENCH {TIER_NAME['tier3_benign_risky']} mean verdict",
        "baybench_score_tier3_lookalikes.png",
        categories,
        series,
        rotate=25,
        fontsize=7,
    )


def plot_family_rules(reports: dict[str, dict], cases) -> None:
    scores = score_by_id(reports)
    catalog = load_catalog()
    rules_by_fam: dict[str, list[str]] = defaultdict(list)
    for rule_id, info in catalog["rules"].items():
        rules_by_fam[info["family"]].append(rule_id)
    t1 = [c for c in cases if c.tier == "tier1_pairs"]
    for fam, rules in rules_by_fam.items():
        columns: list[tuple[str, list[str]]] = []
        for rule in rules:
            ids = [c.id for c in t1 if rule in c.expected_rule_ids or c.id.startswith(f"tier1/{rule}/")]
            if ids:
                columns.append((rule, ids))
        if not columns:
            continue
        categories = [RULE_LABEL[rule] for rule, _ in columns]
        series = {
            label: [mean_score(ids, scores[label]) for _, ids in columns]
            for _, label in TOOLS
        }
        wide = len(columns) <= 3
        plot_from_series(
            f"{TIER_NAME['tier1_pairs']} · {FAMILY_NAME[fam]}",
            f"baybench_rules_family_{fam.lower()}.png",
            categories,
            series,
            size="wide" if wide else "twitter",
            rotate=25,
            fontsize=7,
            bottom_in=1.35,
        )


def plot_high_fp(reports: dict[str, dict]) -> None:
    keys = ["tier1_pairs", "tier3_benign_risky"]
    _grouped(
        reports,
        "BAYBENCH high false positive rate by tier",
        "baybench_high_fp_by_tier.png",
        [TIER_NAME[k] for k in keys],
        "per_tier",
        keys,
        "high_fp_rate",
        size="wide",
        subtitle=TIER_GLOSS,
    )


def plot_required_coverage(reports: dict[str, dict], cases) -> None:
    """Share of labeled families hit. On this corpus every malice case has one label,
    so the number equals family recall — computed here from reports, not the grader."""
    labeled = [c for c in cases if c.is_malicious and c.expected_families]
    by_case = {c.id: c for c in labeled}
    by_tool: dict[str, dict[str, dict]] = {}
    for name, label in TOOLS:
        by_tool[label] = {row["id"]: row for row in reports[name]["scoring"]["cases"]}

    def coverage(ids: list[str], label: str) -> float:
        vals = []
        for case_id in ids:
            fired = set(by_tool[label][case_id]["fired_families"])
            expected = set(by_case[case_id].expected_families)
            vals.append(len(fired & expected) / len(expected))
        return sum(vals) / len(vals)

    tier_keys = ["tier1_pairs", "tier2_realworld"]
    series = {}
    for _, label in TOOLS:
        series[label] = [
            coverage([c.id for c in labeled if c.tier == key], label) for key in tier_keys
        ]
    plot_from_series(
        "Share of required families hit",
        "baybench_required_family_hit.png",
        [TIER_NAME[k] for k in tier_keys],
        series,
        size="wide",
        fontsize=8,
        bottom_in=1.15,
    )

    fams = [f for f in "ABCDEFG" if any(f in c.expected_families for c in labeled)]
    series = {}
    for _, label in TOOLS:
        series[label] = [
            coverage([c.id for c in labeled if fam in c.expected_families], label)
            for fam in fams
        ]
    plot_from_series(
        "Share of required families hit, by family",
        "baybench_required_family_hit_by_family.png",
        [FAMILY_NAME[f] for f in fams],
        series,
        bottom_in=1.35,
    )


def plot_families_fired(reports: dict[str, dict], cases) -> None:
    labeled = [c for c in cases if c.is_malicious and c.expected_families]
    buckets = ("0", "1", "2", "3+")
    series: dict[str, list[float]] = {}
    for name, label in TOOLS:
        by_id = {row["id"]: row for row in reports[name]["scoring"]["cases"]}
        counts = {b: 0 for b in buckets}
        for case in labeled:
            n = len(by_id[case.id]["fired_families"])
            key = "0" if n == 0 else "1" if n == 1 else "2" if n == 2 else "3+"
            counts[key] += 1
        series[label] = [counts[b] / len(labeled) for b in buckets]
    plot_from_series(
        "Families fired per labeled-malice case",
        "baybench_families_fired.png",
        buckets,
        series,
        size="wide",
        fontsize=8,
        bottom_in=0.85,
    )


def main() -> None:
    reports = {name: load_report(name) for name, _ in TOOLS}
    counts = {label: reports[name]["n_cases"] for name, label in TOOLS}
    if len(set(counts.values())) != 1:
        raise SystemExit(f"case-count mismatch: {counts}")
    cases = load_cases(ROOT / "cases", ["1", "2", "3"])
    plot_weighted(reports)
    plot_tier(reports)
    plot_family(reports)
    plot_recall_tier(reports)
    plot_recall_family(reports)
    plot_high_fp(reports)
    plot_tier_families(reports, cases)
    plot_tier3_lookalikes(reports, cases)
    plot_family_rules(reports, cases)
    plot_required_coverage(reports, cases)
    plot_families_fired(reports, cases)


if __name__ == "__main__":
    main()
