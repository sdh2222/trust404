"""Pure merge-rule tests for tools.ensemble."""

from __future__ import annotations

import pytest

from tools.ensemble import decide, merge_all, merge_bench, merge_judge

M = "MALICIOUS"
B = "BENIGN"
U = "UNCERTAIN"


@pytest.mark.parametrize(
    "d,n,expected",
    [
        (M, M, M),
        (M, B, M),
        (M, U, M),
        (M, None, M),
        (B, M, M),
        (U, M, M),
        (None, M, M),
        (B, B, B),
        (B, U, B),
        (B, None, B),
        (U, B, U),
        (None, B, U),
        (U, U, U),
        (None, None, U),
        ("garbage", "BENIGN", U),
        ("benign", "uncertain", B),
    ],
)
def test_decide_table(d: str | None, n: str | None, expected: str) -> None:
    assert decide(d, n) == expected


def test_merge_judge_malicious_from_noexit_only() -> None:
    d_row = {
        "file": "a.sol",
        "verdict": "UNCERTAIN",
        "reasons": ["compile failed: x"],
        "evidence": [],
    }
    n_row = {
        "file": "a.sol",
        "verdict": "MALICIOUS",
        "reasons": ["hidden mint"],
        "evidence": [{"function": "mint", "line": 12}],
    }
    out = merge_judge("a.sol", d_row, n_row)
    assert out["verdict"] == "MALICIOUS"
    assert out["reasons"] == ["hidden mint"]
    assert out["evidence"] == [{"function": "mint", "line": 12}]


def test_merge_judge_benign_only_from_detector() -> None:
    d_row = {
        "file": "a.sol",
        "verdict": "UNCERTAIN",
        "reasons": ["compile failed"],
        "evidence": [],
    }
    n_row = {
        "file": "a.sol",
        "verdict": "BENIGN",
        "reasons": ["nothing found"],
        "evidence": [],
    }
    out = merge_judge("a.sol", d_row, n_row)
    assert out["verdict"] == "UNCERTAIN"
    assert out["reasons"] == ["compile failed", "nothing found"]


def test_merge_judge_both_benign_union() -> None:
    d_row = {
        "file": "a.sol",
        "verdict": "BENIGN",
        "reasons": ["a"],
        "evidence": [],
    }
    n_row = {
        "file": "a.sol",
        "verdict": "BENIGN",
        "reasons": ["b", "a"],
        "evidence": [],
    }
    out = merge_judge("a.sol", d_row, n_row)
    assert out["verdict"] == "BENIGN"
    assert out["reasons"] == ["a", "b"]


def test_merge_judge_malicious_without_evidence_downgrades() -> None:
    d_row = {
        "file": "a.sol",
        "verdict": "BENIGN",
        "reasons": ["clean"],
        "evidence": [],
    }
    n_row = {
        "file": "a.sol",
        "verdict": "MALICIOUS",
        "reasons": [],
        "evidence": [],
    }
    out = merge_judge("a.sol", d_row, n_row)
    assert out["verdict"] == "UNCERTAIN"
    assert out["reasons"][0] == (
        "An engine flagged this file as malicious but produced no code location; "
        "downgraded to UNCERTAIN."
    )


def test_merge_judge_evidence_cleaning() -> None:
    d_row = {
        "file": "a.sol",
        "verdict": "MALICIOUS",
        "reasons": ["hit"],
        "evidence": [
            {"function": ""},
            {"line": 0},
            {"foo": 1},
            {"function": "f", "line": 3},
        ],
    }
    n_row = {
        "file": "a.sol",
        "verdict": "BENIGN",
        "reasons": [],
        "evidence": [],
    }
    out = merge_judge("a.sol", d_row, n_row)
    assert out["evidence"] == [{"function": "f", "line": 3}]


def test_merge_judge_optional_fields_from_first_voter() -> None:
    d_row = {
        "file": "a.sol",
        "verdict": "MALICIOUS",
        "reasons": ["d"],
        "evidence": [{"function": "f", "line": 1}],
        "risk_level": "HIGH",
    }
    n_row = {
        "file": "a.sol",
        "verdict": "MALICIOUS",
        "reasons": ["n"],
        "evidence": [{"function": "g", "line": 2}],
        "risk_level": "CRITICAL",
    }
    out = merge_judge("a.sol", d_row, n_row)
    assert out["risk_level"] == "HIGH"


def test_merge_bench_findings_union_and_reason() -> None:
    finding = {"rule_id": "BAL_PRIV_MINT", "family": "B", "severity": "HIGH"}
    out = merge_bench(
        "a.sol",
        {
            "file": "a.sol",
            "verdict": "Uncertain",
            "reason": "compile_failed: boom",
            "findings": [],
        },
        {
            "file": "a.sol",
            "verdict": "Malicious",
            "findings": [finding],
        },
    )
    assert out["verdict"] == "Malicious"
    assert out["findings"] == [finding]
    assert "reason" not in out

    out_u = merge_bench(
        "a.sol",
        {
            "file": "a.sol",
            "verdict": "Uncertain",
            "reason": "R",
            "findings": [],
        },
        {
            "file": "a.sol",
            "verdict": "Uncertain",
            "findings": [],
        },
    )
    assert out_u["verdict"] == "Uncertain"
    assert out_u["reason"] == "R"


def test_merge_all_single_alive_malicious_without_evidence_downgrades() -> None:
    n_map = {
        "a.sol": {
            "file": "a.sol",
            "verdict": "MALICIOUS",
            "reasons": ["hidden mint"],
            "evidence": [{"foo": 1}],
        }
    }
    rows = merge_all(["a.sol"], None, n_map)
    assert len(rows) == 1
    assert rows[0]["verdict"] == "UNCERTAIN"
    assert rows[0]["reasons"][0] == (
        "An engine flagged this file as malicious but produced no code location; "
        "downgraded to UNCERTAIN."
    )


def test_merge_all_single_alive_engine_passthrough() -> None:
    n_map = {
        "a.sol": {
            "file": "a.sol",
            "verdict": "BENIGN",
            "reasons": ["nothing found"],
            "evidence": [],
        }
    }
    rows = merge_all(["a.sol"], None, n_map)
    assert len(rows) == 1
    assert rows[0]["verdict"] == "BENIGN"
    assert rows[0]["file"] == "a.sol"


def test_merge_all_none_alive() -> None:
    rows = merge_all(["a.sol"], None, None)
    assert len(rows) == 1
    assert rows[0]["file"] == "a.sol"
    assert rows[0]["verdict"] == "UNCERTAIN"
    assert rows[0]["reasons"] == [
        "Both engines failed or timed out; no verdict could be produced."
    ]
    assert rows[0]["evidence"] == []
