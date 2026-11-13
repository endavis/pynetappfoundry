"""Doit tasks for the console_openapi build-time tool."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any


def _run_refresh(ref: str) -> list[list[str]]:
    """Build the argv for the refresh action with the user-supplied ref."""
    cmd = ["uv", "run", "python", "-m", "tools.console_openapi.cli", "build"]
    if ref:
        cmd.extend(["--ref", ref])
    return [cmd]


def task_console_openapi_refresh() -> dict[str, Any]:
    """Regenerate tools/console_openapi/generated/console_openapi.yaml from upstream docs.

    Pass a full commit SHA with ``--ref`` so the lockfile pin is reproducible.
    """

    def action(ref: str) -> None:
        import subprocess  # nosec B404  # subprocess is required for doit tasks

        cmd = _run_refresh(ref)[0]
        subprocess.run(cmd, check=True)

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
    # Pinned to the 0.86 default; a later release switches the default to
    # ``builtin``, which would change the generated output (#825).
    "--formatters",
    "black",
    "isort",
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
    import subprocess  # nosec B404  # subprocess is required for doit tasks

    if not _CONSOLE_SPEC.exists():
        raise FileNotFoundError(
            f"Console OpenAPI spec missing at {_CONSOLE_SPEC}; "
            "run 'doit console_openapi_refresh' first."
        )

    # The tree is wholly generated, so clear it first: a module the generator
    # no longer produces then shows up as a deletion instead of lingering.
    shutil.rmtree(_CONSOLE_MODELS_DIR, ignore_errors=True)
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
    subprocess.run(cmd, check=True)

    # Mirror the post-processing performed by ``doit generate_models``: format
    # first, then auto-fix lint findings the formatter just made redundant
    # (E501 noqa headers, etc.). Run with ``check=False`` because ruff
    # returns non-zero when it has fixed things — that is the intended
    # outcome here.
    subprocess.run(
        ["uv", "run", "ruff", "format", str(_CONSOLE_MODELS_DIR)],
        check=False,
    )
    subprocess.run(
        ["uv", "run", "ruff", "check", "--fix", str(_CONSOLE_MODELS_DIR)],
        check=False,
    )


def task_console_models() -> dict[str, Any]:
    """Generate Pydantic v2 models from the Console OpenAPI spec.

    Reads ``tools/console_openapi/generated/console_openapi.yaml`` and emits
    a tree under ``src/pynetappfoundry/models/console/`` (subdivided into
    ``tenancy/``, ``tenancyv4/`` and ``cvo/`` packages by
    ``datamodel-code-generator``).
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
    the generated tree: it regenerates the output and fails if git reports
    any change under it, whether a modified, deleted or new untracked file
    (#825). It is **not** wired into ``doit check``, which stays fast; the
    ``console-models`` job in CI runs it on every pull request.
    """
    return {
        "actions": [_generate_console_models, _check_models_unchanged],
        "verbosity": 2,
    }


# --- Typed client operations from the Console OpenAPI spec (#735) ------------

_CONSOLE_CLIENT_DIR = Path("src/pynetappfoundry/clients/console/generated")


def _generate_console_client() -> None:
    """Render the Console client operation classes, then format and lint them."""
    import subprocess  # nosec B404  # subprocess is required for doit tasks

    from tools.console_openapi import client_codegen

    if not _CONSOLE_SPEC.exists():
        raise FileNotFoundError(
            f"Console OpenAPI spec missing at {_CONSOLE_SPEC}; "
            "run 'doit console_openapi_refresh' first."
        )

    # Wholly generated, so clear it first: a module the generator no longer
    # produces then shows up as a deletion instead of lingering.
    shutil.rmtree(_CONSOLE_CLIENT_DIR, ignore_errors=True)
    client_codegen.generate(
        _CONSOLE_CLIENT_DIR,
        spec_path=_CONSOLE_SPEC,
        models_root=_CONSOLE_MODELS_DIR,
    )
    # ruff exits non-zero when it fixes things, which is the intended outcome.
    subprocess.run(["uv", "run", "ruff", "format", str(_CONSOLE_CLIENT_DIR)], check=False)
    subprocess.run(
        ["uv", "run", "ruff", "check", "--fix", str(_CONSOLE_CLIENT_DIR)],
        check=False,
    )


def task_console_client() -> dict[str, Any]:
    """Generate the typed Console client operations from the spec and the manifest.

    Reads ``tools/console_openapi/client_ops.toml`` and the committed spec and
    emits ``src/pynetappfoundry/clients/console/generated/``. Run
    ``doit console_models`` first when the models changed.
    """
    return {
        "actions": [_generate_console_client],
        "verbosity": 2,
    }


def task_console_client_check() -> dict[str, Any]:
    """Verify the checked-in Console client operations match a fresh codegen run.

    Regenerates the output and fails if git reports any change under it. Like
    ``console_models_check`` it is not wired into ``doit check``; the
    ``console-models`` job in CI runs it on every pull request.
    """

    def check() -> bool:
        return _check_models_unchanged(_CONSOLE_CLIENT_DIR)

    return {
        "actions": [_generate_console_client, check],
        "verbosity": 2,
    }


def _check_models_unchanged(models_dir: Path = _CONSOLE_MODELS_DIR) -> bool:
    """Return False, printing the changes, if git sees any change under *models_dir*.

    ``git diff`` only sees tracked files, so a new module from the generator
    would pass it. ``git status --porcelain --untracked-files=all`` also
    lists untracked files.
    """
    import subprocess  # nosec B404  # subprocess is required for doit tasks

    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", str(models_dir)],
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(f"Generated Console models differ from the committed tree:\n{result.stdout}")
        return False
    return True
