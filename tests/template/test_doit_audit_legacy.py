"""Tests for tools/doit/audit_legacy.py.

Covers:
- Pattern detection on synthetic files (A-E)
- Comment-line guard (B/C/D)
- Multi-line paren-balanced config= suppression (C/D)
- Allowlist behaviour and path normalisation
- Output / flag semantics (_run_audit, render_json, task_audit_legacy)
- Live-tree regression anchor (scan_tree(_SRC_ROOT))

Tests call the module functions directly — no subprocess.
Match style of tests/template/test_doit_quality.py.
"""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import patch

from tools.doit.audit_legacy import (
    _ALLOWLIST,
    _PATTERNS,
    _SRC_ROOT,
    LegacyMatch,
    _has_config_within_call,
    _run_audit,
    render_json,
    scan_file,
    scan_tree,
    task_audit_legacy,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write(tmp_path: Path, rel: str, content: str) -> Path:
    """Write *content* to *tmp_path*/*rel* and return the absolute Path."""
    target = tmp_path / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


# ---------------------------------------------------------------------------
# _has_config_within_call
# ---------------------------------------------------------------------------


class TestHasConfigWithinCall:
    """Unit tests for the paren-balanced config= forward-window."""

    def test_single_line_with_config(self) -> None:
        lines = ["    client = ONTAPAPIClient(cluster=x, config=c)"]
        assert _has_config_within_call(lines, 0) is True

    def test_single_line_without_config(self) -> None:
        lines = ["    client = ONTAPAPIClient(cluster=x)"]
        assert _has_config_within_call(lines, 0) is False

    def test_multi_line_config_on_later_line(self) -> None:
        lines = [
            "    client = ONTAPAPIClient(",
            "        cluster=x,",
            "        config=cfg,",
            "    )",
        ]
        assert _has_config_within_call(lines, 0) is True

    def test_multi_line_without_config(self) -> None:
        lines = [
            "    client = ONTAPAPIClient(",
            "        cluster=x,",
            "    )",
        ]
        assert _has_config_within_call(lines, 0) is False

    def test_nested_parens_with_config(self) -> None:
        lines = [
            "    client = ONTAPAPIClient(",
            "        cluster=Cluster(ip),",
            "        config=cfg,",
            "    )",
        ]
        assert _has_config_within_call(lines, 0) is True

    def test_config_after_close_not_matched(self) -> None:
        lines = [
            "    client = ONTAPAPIClient(cluster=x)",
            "    config = something",
        ]
        # config= appears after the call closes — must return False
        assert _has_config_within_call(lines, 0) is False


# ---------------------------------------------------------------------------
# Pattern A — Legacy SDK import
# ---------------------------------------------------------------------------


class TestPatternA:
    """Pattern A: from/import netapp_ontap at top-level or indented."""

    def test_top_level_from_import(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "from netapp_ontap.x import Y\n")
        matches = scan_file(p)
        assert len(matches) == 1
        assert matches[0].pattern == "A"
        assert matches[0].line == 1

    def test_top_level_bare_import(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "import netapp_ontap.error\n")
        matches = scan_file(p)
        assert len(matches) == 1
        assert matches[0].pattern == "A"

    def test_indented_from_import_matches(self, tmp_path: Path) -> None:
        """Indented imports (inside functions) must still be detected."""
        content = "def f():\n    from netapp_ontap import X\n"
        p = _write(tmp_path, "foo.py", content)
        matches = scan_file(p)
        assert len(matches) == 1
        assert matches[0].pattern == "A"
        assert matches[0].line == 2

    def test_non_netapp_import_not_matched(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "from netapp_other import X\n")
        matches = scan_file(p)
        assert matches == []


# ---------------------------------------------------------------------------
# Pattern B — HostConnection( call
# ---------------------------------------------------------------------------


class TestPatternB:
    """Pattern B: HostConnection( with comment-line guard."""

    def test_detected(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "    with HostConnection(\n")
        matches = scan_file(p)
        pat_b = [m for m in matches if m.pattern == "B"]
        assert len(pat_b) == 1
        assert pat_b[0].line == 1

    def test_comment_line_suppressed(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "    # HostConnection(host, user)\n")
        matches = scan_file(p)
        pat_b = [m for m in matches if m.pattern == "B"]
        assert pat_b == []

    def test_no_paren_not_matched(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "    conn = HostConnection\n")
        matches = scan_file(p)
        pat_b = [m for m in matches if m.pattern == "B"]
        assert pat_b == []


# ---------------------------------------------------------------------------
# Pattern C — ONTAPAPIClient( without config=
# ---------------------------------------------------------------------------


class TestPatternC:
    """Pattern C: ONTAPAPIClient( with config= suppression."""

    def test_single_line_with_config_suppressed(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "    c = ONTAPAPIClient(cluster=x, config=cfg)\n")
        matches = scan_file(p)
        pat_c = [m for m in matches if m.pattern == "C"]
        assert pat_c == []

    def test_multi_line_with_config_suppressed(self, tmp_path: Path) -> None:
        content = "    c = ONTAPAPIClient(\n        cluster=x,\n        config=cfg,\n    )\n"
        p = _write(tmp_path, "foo.py", content)
        matches = scan_file(p)
        pat_c = [m for m in matches if m.pattern == "C"]
        assert pat_c == []

    def test_single_line_without_config_flagged(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "    c = ONTAPAPIClient(cluster=x)\n")
        matches = scan_file(p)
        pat_c = [m for m in matches if m.pattern == "C"]
        assert len(pat_c) == 1
        assert pat_c[0].line == 1

    def test_comment_line_suppressed(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "    # ONTAPAPIClient(cluster=x)\n")
        matches = scan_file(p)
        pat_c = [m for m in matches if m.pattern == "C"]
        assert pat_c == []

    def test_real_inspect_multi_line_pattern(self, tmp_path: Path) -> None:
        """Reproduces inspect.py:332 multi-line call — must be suppressed."""
        content = (
            "    api_client = ONTAPAPIClient(\n"
            "        cluster=_ClusterObj(cluster, ip),\n"
            "        config=config,\n"
            "    )\n"
        )
        p = _write(tmp_path, "foo.py", content)
        matches = scan_file(p)
        pat_c = [m for m in matches if m.pattern == "C"]
        assert pat_c == []

    def test_class_definition_not_flagged(self, tmp_path: Path) -> None:
        """`class ONTAPAPIClient(APIWrapper):` is a declaration, not a call."""
        p = _write(tmp_path, "foo.py", "class ONTAPAPIClient(APIWrapper):\n    pass\n")
        matches = scan_file(p)
        assert [m for m in matches if m.pattern == "C"] == []

    def test_subclass_of_target_not_flagged(self, tmp_path: Path) -> None:
        """`class Foo(QuerySet):` is a subclass declaration, not a constructor call."""
        p = _write(tmp_path, "foo.py", "class Foo(QuerySet):\n    pass\n")
        matches = scan_file(p)
        assert [m for m in matches if m.pattern == "D"] == []


# ---------------------------------------------------------------------------
# Pattern D — QuerySet( without config=
# ---------------------------------------------------------------------------


class TestPatternD:
    """Pattern D: QuerySet( with config= suppression — mirrors C tests."""

    def test_single_line_with_config_suppressed(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "    qs = QuerySet(Model, client, config=cfg)\n")
        matches = scan_file(p)
        pat_d = [m for m in matches if m.pattern == "D"]
        assert pat_d == []

    def test_multi_line_with_config_suppressed(self, tmp_path: Path) -> None:
        content = (
            "    qs = QuerySet(\n        Model,\n        client,\n        config=cfg,\n    )\n"
        )
        p = _write(tmp_path, "foo.py", content)
        matches = scan_file(p)
        pat_d = [m for m in matches if m.pattern == "D"]
        assert pat_d == []

    def test_single_line_without_config_flagged(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "    qs = QuerySet(Model, client)\n")
        matches = scan_file(p)
        pat_d = [m for m in matches if m.pattern == "D"]
        assert len(pat_d) == 1

    def test_comment_line_suppressed(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "foo.py", "    # QuerySet(Model, client)\n")
        matches = scan_file(p)
        pat_d = [m for m in matches if m.pattern == "D"]
        assert pat_d == []


# ---------------------------------------------------------------------------
# Pattern E — Legacy cache fetch in CLI
# ---------------------------------------------------------------------------


class TestPatternE:
    """Pattern E: only fires under cli/ subtree."""

    def test_detected_under_cli(self, tmp_path: Path) -> None:
        """Pattern E fires when the file is under cli/."""
        # scan_file uses the path to derive rel; we need to place it under
        # a parent that looks like _SRC_ROOT / cli/
        src = tmp_path / "pynetappfoundry"
        p = _write(src, "cli/commands/foo.py", "from pynetappfoundry.cache import fetch\n")
        # Temporarily patch _SRC_ROOT so scan_file resolves the rel path correctly
        with patch("tools.doit.audit_legacy._SRC_ROOT", src):
            matches = scan_file(p)
        pat_e = [m for m in matches if m.pattern == "E"]
        assert len(pat_e) == 1

    def test_not_detected_outside_cli(self, tmp_path: Path) -> None:
        """Pattern E must NOT fire outside cli/."""
        src = tmp_path / "pynetappfoundry"
        p = _write(src, "data/foo.py", "from pynetappfoundry.cache import fetch\n")
        with patch("tools.doit.audit_legacy._SRC_ROOT", src):
            matches = scan_file(p)
        pat_e = [m for m in matches if m.pattern == "E"]
        assert pat_e == []


# ---------------------------------------------------------------------------
# Allowlist behaviour
# ---------------------------------------------------------------------------


class TestAllowlist:
    """scan_tree splits hits into candidates vs legitimate by allowlist."""

    def test_allowlisted_file_in_legitimate(self, tmp_path: Path) -> None:
        src = tmp_path / "pynetappfoundry"
        # Use a path that IS in the allowlist
        _write(src, "clients/ontap/cli.py", "from netapp_ontap import HostConnection\n")
        with patch("tools.doit.audit_legacy._SRC_ROOT", src):
            candidates, legitimate = scan_tree(src)
        assert any(m.file == "clients/ontap/cli.py" for m in legitimate)
        assert not any(m.file == "clients/ontap/cli.py" for m in candidates)

    def test_non_allowlisted_file_in_candidates(self, tmp_path: Path) -> None:
        src = tmp_path / "pynetappfoundry"
        _write(src, "cli/commands/events/get.py", "from netapp_ontap.x import Y\n")
        with patch("tools.doit.audit_legacy._SRC_ROOT", src):
            candidates, _ = scan_tree(src)
        assert any(m.file == "cli/commands/events/get.py" for m in candidates)

    def test_allowlist_path_normalisation(self, tmp_path: Path) -> None:
        """Paths must be posix-form relative to _SRC_ROOT in the returned matches."""
        src = tmp_path / "pynetappfoundry"
        _write(src, "cli/commands/events/get.py", "from netapp_ontap.x import Y\n")
        with patch("tools.doit.audit_legacy._SRC_ROOT", src):
            candidates, _ = scan_tree(src)
        # All file fields must be posix-relative strings (no abs path, no backslash)
        for m in candidates:
            assert not m.file.startswith("/"), f"Absolute path leaked: {m.file}"
            assert "\\" not in m.file, f"Backslash in path: {m.file}"


# ---------------------------------------------------------------------------
# _run_audit return-value semantics
# ---------------------------------------------------------------------------


class TestRunAudit:
    """_run_audit return-value and strict-mode semantics."""

    def _make_matches(self) -> list[LegacyMatch]:
        return [LegacyMatch(file="x.py", line=1, pattern="A", match="from netapp_ontap...")]

    def test_strict_false_always_returns_true(self) -> None:
        with (
            patch("tools.doit.audit_legacy.scan_tree") as mock_scan,
            patch("tools.doit.audit_legacy.render_table"),
        ):
            mock_scan.return_value = (self._make_matches(), [])
            result = _run_audit(strict=False, json_output=False)
        assert result is True

    def test_strict_true_with_candidates_returns_false(self) -> None:
        with (
            patch("tools.doit.audit_legacy.scan_tree") as mock_scan,
            patch("tools.doit.audit_legacy.render_table"),
        ):
            mock_scan.return_value = (self._make_matches(), [])
            result = _run_audit(strict=True, json_output=False)
        assert result is False

    def test_strict_true_no_candidates_returns_true(self) -> None:
        with (
            patch("tools.doit.audit_legacy.scan_tree") as mock_scan,
            patch("tools.doit.audit_legacy.render_table"),
        ):
            mock_scan.return_value = ([], [])
            result = _run_audit(strict=True, json_output=False)
        assert result is True


# ---------------------------------------------------------------------------
# render_json schema
# ---------------------------------------------------------------------------


class TestRenderJson:
    """render_json must emit valid JSON with the documented schema."""

    def _run_render(
        self,
        candidates: list[LegacyMatch],
        legitimate: list[LegacyMatch],
        strict: bool = False,
    ) -> dict[str, Any]:
        buf = StringIO()
        with patch("builtins.print", side_effect=lambda s: buf.write(s + "\n")):
            render_json(candidates, legitimate, strict)
        return json.loads(buf.getvalue())

    def test_top_level_keys(self) -> None:
        data = self._run_render([], [])
        assert "schema_version" in data
        assert "strict" in data
        assert "candidates" in data
        assert "legitimate" in data
        assert "summary" in data

    def test_schema_version_is_1(self) -> None:
        data = self._run_render([], [])
        assert data["schema_version"] == 1

    def test_strict_flag_reflected(self) -> None:
        assert self._run_render([], [], strict=True)["strict"] is True
        assert self._run_render([], [], strict=False)["strict"] is False

    def test_summary_counts_correct(self) -> None:
        c = [LegacyMatch("a.py", 1, "A", "x"), LegacyMatch("b.py", 2, "B", "y")]
        leg = [LegacyMatch("c.py", 3, "A", "z")]
        summary = self._run_render(c, leg)["summary"]
        assert summary["candidate_count"] == 2
        assert summary["legitimate_count"] == 1
        assert summary["allowlist_count"] == len(_ALLOWLIST)

    def test_summary_patterns_has_all_ids(self) -> None:
        patterns = self._run_render([], [])["summary"]["patterns"]
        expected_ids = {pid for pid, _, _ in _PATTERNS}
        assert set(patterns.keys()) == expected_ids

    def test_pattern_counts_in_summary(self) -> None:
        c = [
            LegacyMatch("a.py", 1, "A", "x"),
            LegacyMatch("b.py", 2, "A", "y"),
            LegacyMatch("c.py", 3, "B", "z"),
        ]
        patterns = self._run_render(c, [])["summary"]["patterns"]
        assert patterns["A"] == 2
        assert patterns["B"] == 1
        assert patterns["C"] == 0


# ---------------------------------------------------------------------------
# task_audit_legacy structure
# ---------------------------------------------------------------------------


class TestTaskAuditLegacy:
    """task_audit_legacy must return the expected doit task dict shape."""

    def test_has_required_keys(self) -> None:
        task = task_audit_legacy()
        assert "actions" in task
        assert "params" in task
        assert "verbosity" in task

    def test_params_has_strict_flag(self) -> None:
        params = task_audit_legacy()["params"]
        names = [p["name"] for p in params]
        assert "strict" in names

    def test_params_has_json_flag(self) -> None:
        params = task_audit_legacy()["params"]
        names = [p["name"] for p in params]
        assert "json_output" in names

    def test_params_strict_uses_long_flag(self) -> None:
        params = task_audit_legacy()["params"]
        strict_param = next(p for p in params if p["name"] == "strict")
        assert strict_param["long"] == "strict"
        assert strict_param["type"] is bool
        assert strict_param["default"] is False

    def test_params_json_uses_long_flag(self) -> None:
        params = task_audit_legacy()["params"]
        json_param = next(p for p in params if p["name"] == "json_output")
        assert json_param["long"] == "json"
        assert json_param["type"] is bool
        assert json_param["default"] is False


# ---------------------------------------------------------------------------
# Live-tree regression anchor
# ---------------------------------------------------------------------------


class TestLiveTreeRegression:
    """Regression anchor: scan_tree(_SRC_ROOT) must match manual ground truth.

    Ground truth from #741 / #742:
    - cli/commands/events/get.py lines 10, 11, 146     (A, A, B)
    - cli/commands/events/azevents.py lines 263, 264, 265, 277  (A, A, A, B)
    Total: 7 candidate match lines, all under cli/commands/events/.

    If a future migration PR removes these files, this test will fail
    intentionally — update the expected count after verifying the migration.
    """

    def test_exactly_7_candidates(self) -> None:
        candidates, _ = scan_tree(_SRC_ROOT)
        assert len(candidates) == 7, (
            f"Expected 7 candidates, got {len(candidates)}. "
            f"Candidates: {[(m.file, m.line, m.pattern) for m in candidates]}"
        )

    def test_all_candidates_under_events(self) -> None:
        candidates, _ = scan_tree(_SRC_ROOT)
        for m in candidates:
            assert m.file.startswith("cli/commands/events/"), (
                f"Unexpected candidate outside events/: {m.file}:{m.line}"
            )

    def test_exactly_3_legitimate_hits(self) -> None:
        """clients/ontap/cli.py has 2 pattern-A imports (lines 13, 14) and 1
        pattern-B HostConnection( call (line 437). The class definition at
        clients/ontap/api.py:20 is excluded by the class-line guard."""
        _, legitimate = scan_tree(_SRC_ROOT)
        assert len(legitimate) == 3, (
            f"Expected 3 legitimate hits, got {len(legitimate)}: "
            f"{[(m.file, m.line, m.pattern) for m in legitimate]}"
        )

    def test_pattern_a_count_is_5(self) -> None:
        candidates, _ = scan_tree(_SRC_ROOT)
        a_count = sum(1 for m in candidates if m.pattern == "A")
        assert a_count == 5, f"Expected 5 pattern-A candidates, got {a_count}"

    def test_pattern_b_count_is_2(self) -> None:
        candidates, _ = scan_tree(_SRC_ROOT)
        b_count = sum(1 for m in candidates if m.pattern == "B")
        assert b_count == 2, f"Expected 2 pattern-B candidates, got {b_count}"

    def test_patterns_c_d_e_are_zero(self) -> None:
        candidates, _ = scan_tree(_SRC_ROOT)
        for pid in ("C", "D", "E"):
            count = sum(1 for m in candidates if m.pattern == pid)
            assert count == 0, f"Expected 0 pattern-{pid} candidates, got {count}"
