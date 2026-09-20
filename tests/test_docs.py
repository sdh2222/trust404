from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
AGENTS = REPO_ROOT / "AGENTS.md"
CLAUDE = REPO_ROOT / "CLAUDE.md"
PYPROJECT = REPO_ROOT / "pyproject.toml"
NOEXIT_PKG = REPO_ROOT / "noexit" / "package.json"
SOLC_VERSIONS = REPO_ROOT / "detector" / "solc_versions.txt"
SETUP_LOCAL = REPO_ROOT / "scripts" / "setup_local.sh"
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
TEAM_RULE = REPO_ROOT / ".cursor" / "rules" / "team-workflow.mdc"

_BACKTICK = re.compile(r"`([^`]+)`")
_FORBIDDEN = re.compile(r"[ <>*{$]")
_PATH_EXT = (".md", ".sh", ".py", ".yaml", ".txt", ".toml", ".json")
_SKIP_PREFIX = ("~", ".bench_work", "/input", "/output")
_SKIP_EXACT = frozenset({"out.json", "<dir>"})


def _prerequisites_section(readme: str) -> str:
    match = re.search(r"(?ms)^### Prerequisites$.*?(?=^### |\Z)", readme)
    assert match is not None, "README is missing a ### Prerequisites section"
    return match.group(0)


def _pathish_tokens(text: str) -> list[str]:
    found: list[str] = []
    for raw in _BACKTICK.findall(text):
        token = raw[:-1] if raw.endswith("/") else raw
        if token in _SKIP_EXACT or token.startswith(_SKIP_PREFIX):
            continue
        if _FORBIDDEN.search(token):
            continue
        if "/" not in token and not token.endswith(_PATH_EXT):
            continue
        found.append(token)
    return found


def test_agents_md_exists_and_short() -> None:
    assert AGENTS.is_file(), "AGENTS.md is missing"
    lines = AGENTS.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= 120, f"AGENTS.md is {len(lines)} lines (max 120)"


def test_claude_md_points_to_agents() -> None:
    assert CLAUDE.is_file(), "CLAUDE.md is missing"
    text = CLAUDE.read_text(encoding="utf-8")
    assert "AGENTS.md" in text, "CLAUDE.md must mention AGENTS.md"


def test_readme_has_prerequisites_section() -> None:
    text = README.read_text(encoding="utf-8")
    pre_match = re.search(r"(?m)^### Prerequisites$", text)
    assert pre_match is not None, "README must contain a ### Prerequisites heading"
    runtime_match = re.search(r"(?m)^### Get the runtime$", text)
    assert runtime_match is not None, "README is missing ### Get the runtime"
    assert pre_match.start() < runtime_match.start(), (
        "### Prerequisites must appear before ### Get the runtime"
    )


def test_readme_front_page_sections() -> None:
    text = README.read_text(encoding="utf-8")
    assert text.startswith("# trust404\n"), "README title must be # trust404"
    assert re.search(r"(?m)^## How it decides$", text), "README is missing ## How it decides"


def test_readme_links_agents_md() -> None:
    text = README.read_text(encoding="utf-8")
    assert "AGENTS.md" in text, "README must mention AGENTS.md"


def test_agents_md_named_paths_exist() -> None:
    text = AGENTS.read_text(encoding="utf-8")
    missing = [
        token
        for token in _pathish_tokens(text)
        if not (REPO_ROOT / token).exists()
    ]
    assert missing == [], f"AGENTS.md names missing paths: {missing}"


def test_python_minimum_matches_pyproject() -> None:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    requires = data["project"]["requires-python"]
    version = re.search(r"(\d+\.\d+)", requires)
    assert version is not None, f"could not parse requires-python: {requires!r}"
    ver = version.group(1)
    prereq = _prerequisites_section(README.read_text(encoding="utf-8"))
    agents = AGENTS.read_text(encoding="utf-8")
    assert "Python" in prereq and ver in prereq, (
        f"README Prerequisites must mention Python {ver}"
    )
    assert "Python" in agents and ver in agents, (
        f"AGENTS.md must mention Python {ver}"
    )


def test_node_minimum_matches_source() -> None:
    pkg = json.loads(NOEXIT_PKG.read_text(encoding="utf-8"))
    readme = README.read_text(encoding="utf-8")
    engines = pkg.get("engines") or {}
    node_spec = engines.get("node")
    if node_spec:
        major = re.search(r"(\d+)", str(node_spec))
        assert major is not None, f"could not parse engines.node: {node_spec!r}"
        assert "Node" in readme and major.group(1) in readme, (
            f"README must mention Node {major.group(1)}"
        )
    else:
        assert "Node 18" in readme, "README must mention Node 18"


def test_solc_count_matches_versions_file() -> None:
    n = sum(1 for line in SOLC_VERSIONS.read_text(encoding="utf-8").splitlines() if line.strip())
    prereq = _prerequisites_section(README.read_text(encoding="utf-8"))
    assert f"{n} solc" in prereq, f"README Prerequisites must contain '{n} solc'"


def test_setup_local_builds_noexit() -> None:
    text = SETUP_LOCAL.read_text(encoding="utf-8")
    assert "npx tsc -p tsconfig.json" in text
    assert "npm ci --ignore-scripts" in text


def test_contributing_and_rule_point_to_agents() -> None:
    contributing = CONTRIBUTING.read_text(encoding="utf-8")
    rule = TEAM_RULE.read_text(encoding="utf-8")
    assert "AGENTS.md" in contributing, "CONTRIBUTING.md must mention AGENTS.md"
    assert "AGENTS.md" in rule, ".cursor/rules/team-workflow.mdc must mention AGENTS.md"
