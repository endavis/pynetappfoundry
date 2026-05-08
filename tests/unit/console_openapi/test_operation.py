"""Tests for the operation-line parser."""

from __future__ import annotations

from tools.console_openapi.parser.operation import find_operation


def test_finds_post_operation() -> None:
    body = (
        "= Title\n"
        "[.api-doc-operation .api-doc-operation-post]#POST# "
        "[.api-doc-code-block]#`/x/y`#\n"
        "Description.\n"
    )
    assert find_operation(body) == ("POST", "/x/y")


def test_finds_delete_operation_with_path_template() -> None:
    body = (
        "[.api-doc-operation .api-doc-operation-delete]#DELETE# "
        "[.api-doc-code-block]#`/folders/{folder_id}`#"
    )
    assert find_operation(body) == ("DELETE", "/folders/{folder_id}")


def test_no_operation_returns_none() -> None:
    body = "= Overview\n\nThis is a prose page.\n"
    assert find_operation(body) is None
