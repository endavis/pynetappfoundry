"""Preconditions for a successful TestPyPI publish.

Two kinds of checks live here:

1. Structural asserts on `.github/workflows/testpypi.yml` — the
   `on.push.tags` glob list must cover the four PEP440 pre-release shapes
   that `commitizen` (used by `doit release --prerelease=...`) actually
   emits, and must NOT use the old semver-only pattern that missed every
   PEP440 tag this project produces (issue #659).
2. Git-tracking invariants — `src/pynetappfoundry/_version.py` is a
   build-time artifact written by `hatch-vcs`; if it is tracked in git,
   every build dirties the working tree and `setuptools-scm` appends a
   `+d<date>` local-version suffix that PyPI rejects (issue #661).

These tests do not execute the workflow — they only verify its shape. See
`tests/test_codeql_workflow.py` for the sibling YAML-structure pattern.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / ".github" / "workflows" / "testpypi.yml"
REPO_ROOT = Path(__file__).parent.parent


def _load_workflow() -> dict[Any, Any]:
    """Load and parse the TestPyPI workflow YAML.

    Return type is ``dict[Any, Any]`` (not ``dict[str, Any]``) because PyYAML
    parses the ``on`` key as the boolean ``True`` (YAML 1.1 alias).

    The explicit ``encoding="utf-8"`` is required for Windows, where the
    default ``locale.getpreferredencoding()`` is ``cp1252`` and chokes on any
    non-ASCII content — see the sibling test file for #430 context.
    """
    content = WORKFLOW_PATH.read_text(encoding="utf-8")
    data: dict[Any, Any] = yaml.safe_load(content)
    return data


class TestPushTagTriggers:
    """The PEP440 pre-release tag patterns must be present; semver-only absent."""

    def _tag_patterns(self) -> list[str]:
        wf = _load_workflow()
        # PyYAML parses bare 'on' as the boolean True.
        on_section = wf.get("on") or wf.get(True)
        assert isinstance(on_section, dict), "workflow must have an 'on' mapping"
        push_section = on_section.get("push")
        assert isinstance(push_section, dict), "workflow must have an 'on.push' mapping"
        tags = push_section.get("tags")
        assert isinstance(tags, list), "workflow must have an 'on.push.tags' list"
        return [str(t) for t in tags]

    def test_alpha_pattern_present(self) -> None:
        """PEP440 alpha tags (e.g. v0.1.0a0) must trigger the workflow."""
        assert "v*a[0-9]*" in self._tag_patterns()

    def test_beta_pattern_present(self) -> None:
        """PEP440 beta tags (e.g. v0.1.0b1) must trigger the workflow."""
        assert "v*b[0-9]*" in self._tag_patterns()

    def test_rc_pattern_present(self) -> None:
        """PEP440 rc tags (e.g. v0.1.0rc0) must trigger the workflow."""
        assert "v*rc[0-9]*" in self._tag_patterns()

    def test_dev_pattern_present(self) -> None:
        """PEP440 dev tags (e.g. v0.1.0.dev2) must trigger the workflow."""
        assert "v*.dev[0-9]*" in self._tag_patterns()

    def test_semver_only_pattern_absent(self) -> None:
        """The old semver-style glob that missed all PEP440 tags must be gone."""
        assert "v*-[a-zA-Z]*" not in self._tag_patterns(), (
            "The old semver-only glob did not match commitizen's PEP440 pre-release "
            "tags (e.g. v0.1.0a0) and must stay out to avoid regressing #659."
        )


class TestVersionFileNotTracked:
    """Regression test for issue #661: ``_version.py`` must not be tracked.

    ``hatch-vcs`` writes the computed version to ``_version.py`` during build.
    If the file is tracked, every build dirties the working tree and
    ``setuptools-scm`` appends a ``+d<YYYYMMDD>`` local-version suffix, which
    PyPI rejects with ``400 Bad Request``. The file is in ``.gitignore`` but
    gitignore has no effect on files already in the index, so the only
    durable guard is this assertion.
    """

    def test_version_py_not_tracked(self) -> None:
        """``git ls-files`` must not report src/pynetappfoundry/_version.py."""
        result = subprocess.run(  # nosec B603 B607
            ["git", "ls-files", "--error-unmatch", "src/pynetappfoundry/_version.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode != 0, (
            "src/pynetappfoundry/_version.py is tracked in git (see #661). "
            "It's a build-time artifact written by hatch-vcs. "
            "Fix: git rm --cached src/pynetappfoundry/_version.py"
        )
