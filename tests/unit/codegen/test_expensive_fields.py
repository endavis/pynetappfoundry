"""Tests for expensive field extraction from ONTAP endpoint descriptions."""

from __future__ import annotations

from tools.codegen.expensive_fields import extract_expensive_patterns, is_field_expensive


class TestExtractExpensivePatterns:
    """Tests for extract_expensive_patterns."""

    def test_ontap_volume_style(self):
        """Parses standard ONTAP expensive properties section."""
        desc = (
            "Retrieves volumes.\n"
            "### Expensive properties\n"
            "There is an added computational cost.\n"
            "* `is_svm_root`\n"
            "* `analytics.*`\n"
            "* `autosize.*`\n"
            "* `clone.parent_snapshot.name`\n"
            "### Related Links\n"
            "Some other section.\n"
        )
        patterns = extract_expensive_patterns(desc)
        assert "is_svm_root" in patterns
        assert "analytics.*" in patterns
        assert "autosize.*" in patterns
        assert "clone.parent_snapshot.name" in patterns
        assert len(patterns) == 4

    def test_no_expensive_section(self):
        """Returns empty when no expensive section exists."""
        assert extract_expensive_patterns("Just a description.") == []
        assert extract_expensive_patterns("") == []

    def test_case_insensitive_header(self):
        """Header matching is case-insensitive."""
        desc = "### expensive properties\n* `foo`\n"
        assert extract_expensive_patterns(desc) == ["foo"]

    def test_stops_at_next_header(self):
        """Patterns after the next markdown header are excluded."""
        desc = (
            "### Expensive properties\n* `expensive_field`\n### Other section\n* `not_expensive`\n"
        )
        patterns = extract_expensive_patterns(desc)
        assert patterns == ["expensive_field"]

    def test_multiline_patterns(self):
        """Multiple patterns across lines are all captured."""
        desc = "### Expensive properties\n* `a.*`\n* `b.*`\n* `c`\n"
        assert extract_expensive_patterns(desc) == ["a.*", "b.*", "c"]


class TestIsFieldExpensive:
    """Tests for is_field_expensive matching."""

    def test_exact_match(self):
        """Exact pattern matches exact field."""
        assert is_field_expensive("is_svm_root", ["is_svm_root"])

    def test_wildcard_match_direct(self):
        """Wildcard pattern matches the prefix itself."""
        assert is_field_expensive("analytics", ["analytics.*"])

    def test_wildcard_match_nested(self):
        """Wildcard pattern matches nested fields."""
        assert is_field_expensive("analytics.scan_progress", ["analytics.*"])
        assert is_field_expensive("analytics.foo.bar", ["analytics.*"])

    def test_no_match(self):
        """Non-matching field returns False."""
        assert not is_field_expensive("name", ["analytics.*", "is_svm_root"])

    def test_empty_patterns(self):
        """Empty patterns list never matches."""
        assert not is_field_expensive("anything", [])

    def test_partial_name_no_match(self):
        """Wildcard doesn't match partial name prefix."""
        assert not is_field_expensive("analytics_extra", ["analytics.*"])

    def test_exact_pattern_no_wildcard(self):
        """Exact patterns don't match nested fields."""
        assert not is_field_expensive("is_svm_root.nested", ["is_svm_root"])
