"""Tests for github.py doit tasks.

Phase A scope: covers ``_extract_linked_issues`` only. The full upstream test
suite from ``endavis/pyproject-template:tests/template/test_doit_github.py``
will replace this file during Phase B of the template sync (#716), once the
symbols it imports (``_is_transient_gh_error``, etc.) land via the broader
sync.
"""

from tools.doit.github import _extract_linked_issues


class TestExtractLinkedIssues:
    """Tests for ``_extract_linked_issues``.

    Mirrors upstream PR #544 (``Addresses`` regex anchored to start-of-line,
    case-sensitive). Lowercase, uppercase, and mid-sentence variants are
    ignored to prevent misattribution.
    """

    def test_addresses_issue(self) -> None:
        body = "Addresses #123"
        assert _extract_linked_issues(body) == ["123"]

    def test_addresses_lowercase_ignored(self) -> None:
        body = "addresses #456"
        assert _extract_linked_issues(body) == []

    def test_addresses_uppercase_ignored(self) -> None:
        body = "ADDRESSES #789"
        assert _extract_linked_issues(body) == []

    def test_mid_sentence_ignored(self) -> None:
        body = "This PR Addresses #123"
        assert _extract_linked_issues(body) == []

    def test_multiple_addresses(self) -> None:
        body = "Addresses #123\nAddresses #456"
        assert _extract_linked_issues(body) == ["123", "456"]

    def test_duplicate_issues(self) -> None:
        body = "Addresses #123\nAddresses #123"
        assert _extract_linked_issues(body) == ["123"]

    def test_no_match(self) -> None:
        body = "Some random PR body with no issue reference."
        assert _extract_linked_issues(body) == []
