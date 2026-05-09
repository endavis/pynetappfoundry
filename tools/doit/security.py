"""Security-related doit tasks."""

from typing import Any

from doit.tools import title_with_actions

from .base import optional_root_files

# GHSA-r374-rxx8-8654 / CVE-2026-44405: paramiko rsakey.py allows the SHA-1 algorithm.
# Affects all released paramiko versions (<=4.0.0). Fix landed upstream in commit
# a4489456b6f65281e172380cc4826cee5e851dbb but no tagged release exists yet.
# Suppress until paramiko 4.0.1+ ships — see issue #701.
_AUDIT_IGNORED_VULNS = ("GHSA-r374-rxx8-8654",)


def task_audit() -> dict[str, Any]:
    """Run security audit with pip-audit (requires security extras)."""
    ignore_args = " ".join(f"--ignore-vuln {vid}" for vid in _AUDIT_IGNORED_VULNS)
    return {
        "actions": [
            f"uv run pip-audit --skip-editable {ignore_args} || "
            "echo 'pip-audit not installed. Run: uv sync --extra security'"
        ],
        "title": title_with_actions,
    }


def task_security() -> dict[str, Any]:
    """Run security checks with bandit (requires security extras)."""
    return {
        "actions": [
            "uv run bandit -c pyproject.toml -r src/ tools/"
            + optional_root_files("bootstrap.py")
            + " || echo 'bandit not installed. Run: uv sync --extra security'"
        ],
        "title": title_with_actions,
        "verbosity": 0,
    }


def task_licenses() -> dict[str, Any]:
    """Check licenses of dependencies (requires security extras)."""
    return {
        "actions": [
            "uv run pip-licenses --format=markdown --order=license || "
            "echo 'pip-licenses not installed. Run: uv sync --extra security'"
        ],
        "title": title_with_actions,
    }


def task_sbom() -> dict[str, Any]:
    """Generate SBOM in CycloneDX format (requires security extras)."""
    return {
        "actions": [
            "mkdir -p tmp",
            "uv run cyclonedx-py environment --of JSON -o tmp/sbom.json && "
            "uv run cyclonedx-py environment --of XML -o tmp/sbom.xml || "
            "echo 'cyclonedx-py not installed. Run: uv sync --extra security'",
        ],
        "title": title_with_actions,
        "verbosity": 2,
    }
