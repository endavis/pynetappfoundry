"""Doit tasks for the console_openapi build-time tool."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _run_refresh(ref: str) -> list[list[str]]:
    """Build the argv for the refresh action with the user-supplied ref."""
    cmd = ["uv", "run", "python", "-m", "tools.console_openapi.cli", "build"]
    if ref:
        cmd.extend(["--ref", ref])
    return [cmd]


def task_console_openapi_refresh() -> dict[str, Any]:
    """Regenerate tools/console_openapi/generated/console_openapi.yaml from upstream docs."""

    def action(ref: str) -> None:
        import subprocess  # nosec B404

        cmd = _run_refresh(ref)[0]
        subprocess.run(cmd, check=True)  # nosec B603

    return {
        "actions": [action],
        "verbosity": 2,
        "params": [
            {
                "name": "ref",
                "long": "ref",
                "short": "r",
                "default": "main",
                "help": "Git ref to fetch.",
            },
        ],
    }


def task_console_openapi_check() -> dict[str, Any]:
    """Verify the checked-in spec matches a fresh build.

    This task performs a network git-clone of the upstream docs repo and
    a full rebuild, so it is **not** wired into ``doit check`` (which is
    designed to run quickly and offline). Run it explicitly in CI.
    """
    out = Path("tools/console_openapi/generated/console_openapi.yaml")
    return {
        "actions": [
            ["uv", "run", "python", "-m", "tools.console_openapi.cli", "build", "--out", str(out)],
            ["git", "--no-pager", "diff", "--exit-code", "--", str(out.parent)],
        ],
        "verbosity": 2,
    }


# --- Pydantic codegen from the Console OpenAPI spec --------------------------

# Inputs / outputs for the Console Pydantic codegen pipeline. The spec is a
# committed artifact produced by ``doit console_openapi_refresh``; the
# generated tree is committed alongside it.
_CONSOLE_SPEC = Path("tools/console_openapi/generated/console_openapi.yaml")
_CONSOLE_MODELS_DIR = Path("src/pynetappfoundry/models/console")

# ``datamodel-code-generator`` flags pinned for reproducibility. These are
# inlined here (rather than in a separate config file) so the doit task is
# the single source of truth — ``datamodel-codegen`` 0.56.x reads project
# config from ``pyproject.toml`` and would conflict with any future use of
# the tool by other parts of the project. Keep this list ordered the same
# way it appears in the upstream ``--help`` to make diffs reviewable.
_DATAMODEL_CODEGEN_FLAGS: tuple[str, ...] = (
    "--input-file-type",
    "openapi",
    "--output-model-type",
    "pydantic_v2.BaseModel",
    "--target-python-version",
    "3.12",
    "--use-double-quotes",
    "--use-standard-collections",
    "--use-union-operator",
    "--field-constraints",
    "--use-schema-description",
    "--disable-timestamp",
)


def _generate_console_models() -> None:
    """Run ``datamodel-codegen`` and ruff post-processing for Console models."""
    import subprocess  # nosec B404

    if not _CONSOLE_SPEC.exists():
        raise FileNotFoundError(
            f"Console OpenAPI spec missing at {_CONSOLE_SPEC}; "
            "run 'doit console_openapi_refresh' first."
        )

    _CONSOLE_MODELS_DIR.mkdir(parents=True, exist_ok=True)

    cmd: list[str] = [
        "uv",
        "run",
        "datamodel-codegen",
        "--input",
        str(_CONSOLE_SPEC),
        "--output",
        str(_CONSOLE_MODELS_DIR),
        *_DATAMODEL_CODEGEN_FLAGS,
    ]
    subprocess.run(cmd, check=True)  # nosec B603

    # Mirror the post-processing performed by ``doit generate_models``: format
    # first, then auto-fix lint findings the formatter just made redundant
    # (E501 noqa headers, etc.). Run with ``check=False`` because ruff
    # returns non-zero when it has fixed things — that is the intended
    # outcome here.
    subprocess.run(  # nosec B603
        ["uv", "run", "ruff", "format", str(_CONSOLE_MODELS_DIR)],
        check=False,
    )
    subprocess.run(  # nosec B603
        ["uv", "run", "ruff", "check", "--fix", str(_CONSOLE_MODELS_DIR)],
        check=False,
    )


def task_console_models() -> dict[str, Any]:
    """Generate Pydantic v2 models from the Console OpenAPI spec.

    Reads ``tools/console_openapi/generated/console_openapi.yaml`` and emits
    a tree under ``src/pynetappfoundry/models/console/`` (subdivided into
    ``tenancy/`` and ``tenancyv4/`` packages by ``datamodel-code-generator``).
    The generated tree is committed alongside the spec; CI verifies that
    re-running this task is a no-op via ``doit console_models_check``.
    """
    return {
        "actions": [_generate_console_models],
        "verbosity": 2,
    }


def task_console_models_check() -> dict[str, Any]:
    """Verify the checked-in Console models match a fresh codegen run.

    Like ``console_openapi_check``, this task is the determinism guard for
    the generated tree — it regenerates and ``git diff --exit-code``-s the
    output. It is **not** wired into ``doit check`` (which stays fast and
    offline); run it explicitly in CI or before merging changes that touch
    the codegen pipeline or the spec.
    """
    return {
        "actions": [
            _generate_console_models,
            [
                "git",
                "--no-pager",
                "diff",
                "--exit-code",
                "--",
                str(_CONSOLE_MODELS_DIR),
            ],
        ],
        "verbosity": 2,
    }
