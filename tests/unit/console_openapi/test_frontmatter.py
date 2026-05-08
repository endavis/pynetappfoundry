"""Tests for the front-matter parser."""

from __future__ import annotations

from tools.console_openapi.parser.frontmatter import split_frontmatter


def test_extracts_frontmatter() -> None:
    text = "---\napi: true\npermalink: 'a/b.html'\n---\nbody here\n"
    fm, body = split_frontmatter(text)
    assert fm == {"api": True, "permalink": "a/b.html"}
    assert body == "body here\n"


def test_no_frontmatter() -> None:
    text = "= Title\nbody\n"
    fm, body = split_frontmatter(text)
    assert fm == {}
    assert body == text


def test_unterminated_frontmatter_returns_text() -> None:
    text = "---\nfoo: bar\nbaz: qux\n"
    fm, body = split_frontmatter(text)
    assert fm == {}
    assert body == text
