"""CI workflow shape for the published amd64 detector image."""

from __future__ import annotations

import re

import yaml

from tests.detector.conftest import REPO_ROOT

WORKFLOW = REPO_ROOT / ".github" / "workflows" / "detector-image.yml"
USES_RE = re.compile(r"^(actions|docker)/[a-z-]+@v\d+$")


def _walk_uses(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        uses = node.get("uses")
        if isinstance(uses, str):
            found.append(uses)
        for value in node.values():
            found.extend(_walk_uses(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(_walk_uses(item))
    return found


def _run_scripts(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        run = node.get("run")
        if isinstance(run, str):
            found.append(run)
        for value in node.values():
            found.extend(_run_scripts(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(_run_scripts(item))
    return found


def test_detector_image_workflow_shape() -> None:
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert data["permissions"] == {"contents": "write", "packages": "write"}
    on = data["on"]
    assert "workflow_dispatch" in on
    tags = on["push"]["tags"]
    assert "submission-*" in tags
    jobs = data["jobs"]
    assert len(jobs) == 1
    job = next(iter(jobs.values()))
    assert job["runs-on"] == "ubuntu-latest"
    for uses in _walk_uses(data):
        assert USES_RE.match(uses), uses
    for script in _run_scripts(data):
        assert "ghp_" not in script
        assert "ghs_" not in script
        assert "github_pat_" not in script
    joined = "\n".join(_run_scripts(data))
    assert "--network none" in joined


def test_detector_image_workflow_publishes_ensemble() -> None:
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    job = next(iter(data["jobs"].values()))
    steps = job["steps"]
    ensemble_build = None
    for step in steps:
        with_block = step.get("with") or {}
        if with_block.get("file") == "Dockerfile":
            ensemble_build = step
            break
    assert ensemble_build is not None
    build_args = str(ensemble_build["with"].get("build-args", ""))
    assert "BASE=" in build_args
    assert "steps.push.outputs.digest" in build_args
    tags = str(ensemble_build["with"].get("tags", ""))
    assert "trust404-ensemble" in tags
    detector_smoke = None
    ensemble_file = None
    ensemble_smoke = None
    for index, step in enumerate(steps):
        if step.get("name") == "Hardened smoke matrix":
            detector_smoke = index
        with_block = step.get("with") or {}
        if with_block.get("file") == "Dockerfile" and ensemble_file is None:
            ensemble_file = index
        if step.get("name") == "Ensemble hardened smoke":
            ensemble_smoke = index
    assert detector_smoke is not None
    assert ensemble_file is not None
    assert ensemble_smoke is not None
    assert detector_smoke < ensemble_file < ensemble_smoke
    joined = "\n".join(_run_scripts(data))
    assert "trust404-ensemble-amd64.tar.gz" in joined
    assert "ENSEMBLE_MODE=judge" in joined
    assert "JUDGE_SMOKE_REQUIRE_ENGINES=detector,noexit" in joined
    assert "DEGRADED" in joined
    for script in _run_scripts(data):
        assert "docker rmi" not in script
        assert ":hold" not in script


def test_ci_workflow_shape() -> None:
    ci_path = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    data = yaml.safe_load(ci_path.read_text(encoding="utf-8"))
    assert data["permissions"] == {"contents": "read"}
    jobs = data["jobs"]
    assert set(jobs) == {"tests", "ensemble-image"}
    tests_steps = jobs["tests"]["steps"]
    tsc_index = None
    pytest_index = None
    smoke = None
    for index, step in enumerate(tests_steps):
        run = step.get("run")
        if not isinstance(run, str):
            continue
        if "npx tsc -p tsconfig.json" in run and tsc_index is None:
            tsc_index = index
        if run.lstrip().startswith("pytest") and pytest_index is None:
            pytest_index = index
        if "judge_smoke.sh" in run:
            smoke = step
    assert tsc_index is not None
    assert pytest_index is not None
    assert tsc_index < pytest_index
    assert smoke is not None
    assert smoke.get("env", {}).get("JUDGE_SMOKE_REQUIRE_ENGINES") == "detector,noexit"
    ensemble = jobs["ensemble-image"]
    assert ensemble["permissions"] == {"contents": "read", "packages": "read"}
    build = None
    for step in ensemble["steps"]:
        with_block = step.get("with") or {}
        if with_block.get("file") == "Dockerfile":
            build = step
            break
    assert build is not None
    assert build["with"]["push"] is False
    assert build["with"]["load"] is True
    for uses in _walk_uses(data):
        assert USES_RE.match(uses), uses
    for script in _run_scripts(data):
        assert "ghp_" not in script
        assert "ghs_" not in script
        assert "github_pat_" not in script
