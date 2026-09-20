#!/usr/bin/env python3
"""The hand-drawn diagrams in the academic paper.

Requires the exkit toolchain from the `excalidraw-style` skill (exkit.py,
render.mjs, svg2png.py, the @excalidraw/utils npm packages, Excalifont in
~/.fonts and a Playwright Chromium). Run it with EXKIT_DIR pointing at that
directory:

    EXKIT_DIR=<toolchain> <toolchain>/venv/bin/python docs/research/_paper_diagrams.py

It writes both the editable .excalidraw source and the .png into
docs/research/figures/. Both are committed, so the paper builds without the
toolchain; only regenerating a diagram needs it.

Conventions follow the ethtokyo figure set: no title inside the image (the
paper caption carries it), centred box headers with a sub-line, gray
annotations under a box rather than inside it, numbered arrow labels where
there is a sequence, and one color per role held across every figure.

Sizing: the figures render at 92% of a 6.4in text column, so a canvas wider
than about 900 logical px pushes the inner text below 8pt in print. Every
layout here stays inside that budget.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# exkit.py lives in the skill's toolchain directory, not in this repo.
_EXKIT = os.environ.get("EXKIT_DIR")
if _EXKIT:
    sys.path.insert(0, _EXKIT)
import exkit as ek  # noqa: E402

FIG = Path(__file__).resolve().parent / "figures"
FIG.mkdir(exist_ok=True)

# One color per role, held across every figure.
#   blue   the detector's own machinery      purple  state the owner controls
#   orange the user's path and user assets   green   benign or bounded
#   red    malicious                         gray    neutral, harness, abstain
HDR, BODY, NOTE = 18, 16, 13


def under(s, box, text, dy=8, size=NOTE):
    """Gray annotation centred under a box, outside it (ethtokyo convention)."""
    return s.text(box["x"] + box["width"] / 2, box["y"] + box["height"] + dy,
                  text, size, ek.MUTED, align="center")


def over(s, box, text, dy=22, size=NOTE):
    return s.text(box["x"] + box["width"] / 2, box["y"] - dy, text, size, ek.MUTED,
                  align="center")


# --------------------------------------------------------------- 1. predicate
def predicate():
    s = ek.Scene()
    Y, H, W = 46, 132, 250
    a = s.box(20, Y, W, H, "blue", "privileged writer",
              "reachable only when\nmsg.sender equals\na state address",
              label_size=HDR, body_size=BODY, center=True)
    b = s.box(325, Y, W, H, "purple", "writable state",
              "written under that\nprivilege, and by no\nunprivileged function",
              label_size=HDR, body_size=BODY, center=True)
    c = s.box(630, Y, W, H, "orange", "impact on the user",
              "a gate, an amount,\nthe ledger itself, or\nan external call target",
              label_size=HDR, body_size=BODY, center=True)
    s.arrow(a, b, "purple", None, width=3)
    s.arrow(b, c, "orange", None, width=3)
    for box, txt in ((a, "1. who"), (b, "2. what it can set"), (c, "3. what that reaches")):
        over(s, box, txt)
    under(s, b, "all three, or there is no finding")

    s.note(20, Y + H + 58, 860, "gray",
           "No rule compares a user-chosen identifier against a word list. The only anchors are the\n"
           "ERC-20 signatures and Solidity builtins, so renaming the gate does not hide it.",
           size=BODY)
    return s.render(f"{FIG}/baybench_01_predicate.png", scale=3)


# ----------------------------------------------------- 2. transfer path / gate
def transfer_path():
    s = ek.Scene()
    writer = s.box(20, 46, 290, 96, "blue", "a privileged writer",
                   "msg.sender == a state address",
                   label_size=HDR, body_size=BODY, center=True)
    var = s.box(560, 46, 300, 96, "purple", "the gated variable",
                "mapping(address => bool)",
                label_size=HDR, body_size=BODY, center=True)
    under(s, var, "no unprivileged function writes it")
    s.arrow(writer, var, "purple", "1. writes", width=3, label_size=NOTE)

    PY_, PH_ = 270, 88
    t1 = s.box(20, PY_, 200, PH_, "orange", "transfer()", "the user calls",
               label_size=HDR, body_size=BODY, center=True)
    t2 = s.box(300, PY_, 220, PH_, "orange", "_transfer()", "internal callee",
               label_size=HDR, body_size=BODY, center=True)
    t3 = s.box(590, PY_, 240, PH_, "orange", "require(...)", "end node on the path",
               label_size=HDR, body_size=BODY, center=True)
    s.arrow(t1, t2, "ink", None, width=2)
    s.arrow(t2, t3, "ink", None, width=2)
    s.arrow(var, t3, "purple", "2. read here", width=3, label_size=NOTE, bound=False,
            a_anchor=(0.5, 1), b_anchor=(0.5, 0), label_offset=(12, -8))
    over(s, t1, "the path every holder takes")

    s.note(20, PY_ + PH_ + 48, 830, "gray",
           "The path is a call-graph closure, so the check still counts when it sits in a modifier\n"
           "defined in another contract or in a helper two calls deep. Rename every identifier and\n"
           "the same finding fires, because no rule reads the names.",
           size=BODY)
    return s.render(f"{FIG}/baybench_02_transfer_path.png", scale=3)


# ------------------------------------------------------------ 3. verdict ladder
def ladder():
    s = ek.Scene()
    BY, BH, BW = 46, 120, 270
    gov = s.box(290, BY, BW, BH, "gray", "governance",
                "who holds the power\nseverity unchanged",
                label_size=HDR, body_size=BODY, center=True)
    under(s, gov, "managed_role, issuer_token")
    bound = s.box(290, BY + 162, BW, BH, "green", "bounding",
                  "how much power there is\nseverity demoted to INFO",
                  label_size=HDR, body_size=BODY, center=True)
    under(s, bound, "constant_cap, ungate_exists, fee_cap")
    find = s.box(20, BY + 81, 210, BH, "blue", "a finding",
                 "rule, family,\nseverity, evidence", label_size=HDR, body_size=BODY,
                 center=True)
    decide = s.card(630, BY + 54, 230, "ink", "decide()", key_w=112, row_h=34, gap=6,
                    header_size=HDR, body_size=15, rows=[
                        ("1. counting", "Malicious"),
                        ("2. ext. gate", "Uncertain"),
                        ("3. else", "Benign"),
                    ])

    s.arrow(find, gov, "gray", None, width=2)
    s.arrow(find, bound, "green", None, width=2)
    s.arrow(gov, decide, "gray", None, width=3, a_anchor=(1, 0.5), b_anchor=(0, 0.28))
    s.arrow(bound, decide, "green", None, width=3, a_anchor=(1, 0.5), b_anchor=(0, 0.8))

    s.note(20, BY + 330, 840, "orange",
           "The capped mint and the uncapped mint produce the same finding. The bounding\n"
           "discriminator, not the rule, is what separates them.", size=BODY)
    return s.render(f"{FIG}/baybench_03_verdict_ladder.png", scale=3)


# ------------------------------------------------------------ 4. scratch mirror
def scratch_mirror():
    s = ek.Scene()
    ZH, BH = 168, 84
    XS = (44, 264, 484, 704)

    def row(zy, zcol, label, second, third, fourth, fcol, note):
        s.zone(20, zy, 880, ZH, label, color=zcol, label_size=HDR - 2)
        by = zy + 52
        a = s.box(XS[0], by, 180, BH, "gray", "/input", "mounted read only",
                  label_size=HDR - 2, body_size=BODY, center=True)
        b = s.box(XS[1], by, 180, BH, "purple", second[0], second[1],
                  label_size=HDR - 2, body_size=BODY, center=True)
        c = s.box(XS[2], by, 180, BH, "orange", third[0], third[1],
                  label_size=HDR - 2, body_size=BODY, center=True)
        d = s.box(XS[3], by, 180, BH, fcol, fourth[0], fourth[1],
                  label_size=HDR - 2, body_size=BODY, center=True)
        s.arrow(a, b, "ink", None, width=2)
        s.arrow(b, c, "ink", None, width=2)
        s.arrow(c, d, fcol, None, width=3)
        under(s, d, note, dy=6)

    row(20, "red", "before: the rewrite lands beside the source",
        ("ladder rewrite", "relax the pragma"),
        ("write the copy", "into /input"),
        ("analysis_error", "EROFS"), "red",
        "48 files, 35 of them malicious")
    row(252, "green", "after: the rewrite lands in a scratch mirror",
        ("scratch mirror", "hard links, temp dir"),
        ("write the copy", "same relative path"),
        ("compiles", "verdict as local"), "green",
        "0 analysis errors")

    s.note(20, 470, 880, "gray",
           "The grader mounts the input directory read only. The ladder has to rewrite a file to\n"
           "compile an exact pragma, a duplicate SPDX header or a byte-order mark, so the rewrite\n"
           "goes to a mirror of the whole root and never to the root itself.", size=BODY)
    return s.render(f"{FIG}/baybench_04_scratch_mirror.png", scale=3)


# ------------------------------------------------------------------ 5. harness
def harness():
    s = ek.Scene()
    PY_, PH_, PW = 46, 110, 195
    xs = [20, 245, 470, 695]
    boxes = []
    for x, (lab, body, col) in zip(xs, [
        ("cases/", "859 labelled .sol\nin four tiers", "gray"),
        ("the tool", "/input read only\n/output/results.json", "ink"),
        ("results.json", "verdict and\nfindings[]", "gray"),
        ("report.json", "per tier, per family,\n859 case rows", "gray"),
    ]):
        boxes.append(s.box(x, PY_, PW, PH_, col, lab, body, label_size=HDR, body_size=BODY,
                           center=True, stroke_width=3 if col == "ink" else 2))
    for a, b in zip(boxes, boxes[1:]):
        s.arrow(a, b, "ink", None, width=3)
    under(s, boxes[1], "the harness never imports it")

    ZY = 262
    s.zone(95, ZY, 620, 120, "any registered tool: a Docker image or a shell command",
           label_size=HDR - 3)
    for x, col, name in [(120, "blue", "detector"), (270, "green", "noexit"),
                         (420, "red", "Slither"), (570, "purple", "keyword")]:
        s.box(x, ZY + 46, 125, 58, col, name, None, label_size=HDR - 2, center=True)
    s.arrow((405, ZY - 6), (405, PY_ + PH_ + 8), "gray", None, width=2)

    s.note(20, ZY + 152, 870, "orange",
           "Grading parity is fixed at docker run --rm --network none, so a network-dependent tool\n"
           "scores zero by construction. A probe tool in the registry proves the isolation holds.",
           size=BODY)
    return s.render(f"{FIG}/baybench_05_harness.png", scale=3)


# ------------------------------------------------------------------ 6. scoring
def scoring():
    s = ek.Scene()
    case = s.card(20, 62, 250, "gray", "one case", key_w=100, row_h=32, gap=6,
                  header_size=HDR, body_size=15, rows=[
                      ("preferred", "Malicious"),
                      ("accepted", "+ Benign"),
                  ])
    over(s, case, "what the label says", dy=24)

    PH_ = 60
    pills = []
    for i, (col, verdict, score) in enumerate([
        ("green", "the preferred verdict", "1.0"),
        ("green", "another accepted one", "0.75"),
        ("gray", "Uncertain", "0.5"),
        ("red", "anything else", "0.0"),
    ]):
        y = 20 + i * 72
        p = s.box(340, y, 250, PH_, col, verdict, None, label_size=15, center=True)
        s.text(612, y + (PH_ - 22 * 1.25) / 2, score, 22, col, align="left")
        pills.append(p)
    under(s, case, "the tool's verdict is scored\nagainst both of these", dy=8)

    weights = s.card(680, 62, 220, "ink", "tier weight", key_w=118, row_h=32, gap=6,
                     header_size=HDR, body_size=15, rows=[
                         ("0    n=5", "1"),
                         ("1    n=67", "2"),
                         ("2    n=779", "1"),
                         ("3    n=8", "2"),
                     ])
    under(s, weights, "779 paper fixtures must not\ndecide the headline alone", dy=8)

    s.note(20, 340, 880, "orange",
           "The headline is the mean of the per-tier means under those weights, not the mean over\n"
           "cases. Tier 0 also carries a separate gate line, exact out of five, so five public\n"
           "samples stay visible without dominating the number.", size=BODY)
    return s.render(f"{FIG}/baybench_06_scoring.png", scale=3)


# ------------------------------------------------------------- 7. same finding
def same_finding():
    s = ek.Scene()
    COLS = [(30, 220), (280, 200), (510, 170), (720, 160)]
    for (x, w), name in zip(COLS, ["the code", "the finding", "the discriminator", "the verdict"]):
        t = s.text(x + w / 2, 20, name, NOTE + 1, ek.MUTED, align="center")
        t["x"] = x + w / 2 - t["width"] / 2

    ZH, BH = 142, 82

    def row(zy, zcol, zlabel, code, disc, disc_col, dashed, verdict, vcol):
        s.zone(20, zy, 880, ZH, zlabel, color=zcol, label_size=HDR - 3)
        by = zy + 46
        b0 = s.box(COLS[0][0], by, COLS[0][1], BH, "gray", None, code,
                   body_size=BODY, center=True, fill="none")
        b1 = s.box(COLS[1][0], by, COLS[1][1], BH, "orange", "BAL_PRIV_MINT", "family B, HIGH",
                   label_size=HDR - 3, body_size=BODY, center=True)
        b2 = s.box(COLS[2][0], by, COLS[2][1], BH, disc_col, disc, None,
                   label_size=HDR - 3, center=True, dashed=dashed,
                   fill="none" if dashed else "hachure")
        b3 = s.box(COLS[3][0], by, COLS[3][1], BH, vcol, verdict, None,
                   label_size=HDR - 1, center=True)
        for p, q in ((b0, b1), (b1, b2)):
            s.arrow(p, q, "ink", None, width=2)
        s.arrow(b2, b3, vcol, None, width=3)
        return b1

    row(46, "red", "P2_HiddenMint      label MALICIOUS",
        "owner-only mint\nno bound anywhere", "none", "gray", True, "Malicious", "red")
    f2 = row(216, "green", "P4_CappedMint      label BENIGN",
             "owner-only mint\nbounded by a constant", "constant_cap", "green", False,
             "Benign", "green")
    under(s, f2, "identical to the row above", dy=6)

    s.note(20, 400, 880, "gray",
           "Same rule, same family, same base severity, same evidence shape. A detector that reads\n"
           "the finding alone cannot separate these two files; only the discriminator column can.",
           size=BODY)
    return s.render(f"{FIG}/baybench_07_same_finding.png", scale=3)


# ------------------------------------------------------------- 8. family recall
def family_recall():
    s = ek.Scene()
    ZH, BH = 128, 74

    def row(zy, expected, fired, hit, col, note):
        s.zone(20, zy, 880, ZH, None, color=None)
        by = zy + 28
        e = s.box(46, by, 230, BH, "purple", "expected", expected,
                  label_size=HDR - 2, body_size=BODY, center=True)
        f = s.box(340, by, 260, BH, "orange", "families fired", fired,
                  label_size=HDR - 2, body_size=BODY, center=True)
        v = s.box(680, by, 190, BH, col, hit, None, label_size=HDR, center=True)
        s.arrow(e, f, "ink", None, width=2)
        s.arrow(f, v, col, None, width=3)
        under(s, f, note, dy=5)

    row(20, "{ F }", "{ C, D, F }", "hit", "green",
        "the tagged family fired; C and D are extra and unscored")
    row(172, "{ B }", "{ C, D }", "miss", "red",
        "the tagged family never fired, so the case enters the worklist")

    s.note(20, 330, 880, "gray",
           "Family recall is any-hit, not all-hit, and 548 of the 551 labelled-malice cases carry\n"
           "exactly one family tag. A recall of 0.9201 means the tagged family fired on 92 percent\n"
           "of cases. It does not mean 92 percent of the patterns present were listed: the detector\n"
           "fires three or more families on 57 percent of them, and those extras are neither\n"
           "rewarded nor penalised.", size=BODY)
    return s.render(f"{FIG}/baybench_08_family_recall.png", scale=3)


for fn in (predicate, transfer_path, ladder, scratch_mirror,
           harness, scoring, same_finding, family_recall):
    print("wrote", fn())
