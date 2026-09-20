"""CI workflow shape for the published amd64 detector image."""

from __future__ import annotations

import re

import yaml

from tests.detector.conftest import REPO_ROOT

WORKFLOW = REPO_ROOT / ".github" / "workflows" / "detector-image.yml"
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"
USES_RE = re.compile(r"^(actions|docker)/[a-z-]+@v\d+$")
# Env names read by run.sh, tools/ensemble.py, and detector/docker_entry.py.
# Job/step `env:` keys with these names shadow the local-override contract.
RUN_SH_CONTRACT_ENV = frozenset(
    {
        "DETECTOR_IMAGE",
        "ENSEMBLE_IMAGE",
        "DETECTOR_NO_DOCKER",
        "ENSEMBLE_ENGINES",
        "DETECTOR_PYTHON",
        "ENSEMBLE_NODE",
        "DETECTOR_MODE",
        "ENSEMBLE_MODE",
        "ENSEMBLE_BUDGET_S",
        "ENSEMBLE_DETECTOR_BUDGET_S",
        "ENSEMBLE_PYTHON",
    }
)


def _workflow_env_keys(data: dict, *, include_steps: bool) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    top = data.get("env")
    if isinstance(top, dict):
        for key in top:
            found.append(("workflow.env", str(key)))
    jobs = data.get("jobs") or {}
    if not isinstance(jobs, dict):
        return found
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        job_env = job.get("env")
        if isinstance(job_env, dict):
            for key in job_env:
                found.append((f"jobs.{job_name}.env", str(key)))
        if not include_steps:
            continue
        steps = job.get("steps") or []
        if not isinstance(steps, list):
            continue
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            step_env = step.get("env")
            if isinstance(step_env, dict):
                for key in step_env:
                    found.append((f"jobs.{job_name}.steps[{index}].env", str(key)))
    return found


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


def test_publish_workflow_env_does_not_shadow_run_sh_contract() -> None:
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    for location, key in _workflow_env_keys(data, include_steps=True):
        assert key not in RUN_SH_CONTRACT_ENV, (
            f"{location}: {key} shadows run.sh / ensemble.py / docker_entry.py"
        )


def test_ci_workflow_env_does_not_shadow_run_sh_contract() -> None:
    # Step-level env on the judge-smoke step (DETECTOR_PYTHON,
    # JUDGE_SMOKE_REQUIRE_ENGINES) is an intended input; only top-level and
    # job-level env mappings are checked here.
    data = yaml.safe_load(CI_WORKFLOW.read_text(encoding="utf-8"))
    for location, key in _workflow_env_keys(data, include_steps=False):
        assert key not in RUN_SH_CONTRACT_ENV, (
            f"{location}: {key} shadows run.sh / ensemble.py / docker_entry.py"
        )


def test_ci_workflow_shape() -> None:
    data = yaml.safe_load(CI_WORKFLOW.read_text(encoding="utf-8"))
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
