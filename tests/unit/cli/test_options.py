"""Tests for the shared click option decorators and the no-duplicates guard."""

from __future__ import annotations

import ast
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click
import pytest
from click.testing import CliRunner

import pynetappfoundry.cli
from pynetappfoundry.cli.main import nf
from pynetappfoundry.cli.options import (
    ALL_HELP,
    CSV_HELP,
    FILTER_HELP,
    JSON_HELP,
    all_option,
    csv_option,
    filter_option,
    json_option,
)

CLI_DIR = Path(pynetappfoundry.cli.__file__).parent
SHARED_FLAGS = {"--filter", "--json", "--csv", "--all"}
# Whatever this click version reports for an option declared without a default.
_UNSET_DEFAULT = click.Option(["--x"]).default
ALLOWED_LOCAL = {("commands/cifs/session.py", "--csv")}


def _option(decorator: Callable[[Any], Any]) -> click.Option:
    """Apply *decorator* to a throwaway command and return its only option."""

    @click.command()
    @decorator
    def cmd(**kwargs: object) -> None:
        pass

    (opt,) = [p for p in cmd.params if isinstance(p, click.Option)]
    return opt


def _make_cmd(decorator: Callable[[Any], Any]) -> click.Command:
    @click.command()
    @decorator
    def cmd(**kwargs: object) -> None:
        click.echo(repr(sorted(kwargs.items())))

    return cmd


class TestFactories:
    """Tests for the declaration each factory produces."""

    def test_filter_defaults(self) -> None:
        opt = _option(filter_option())
        assert opt.opts == ["--filter", "-f"]
        assert opt.name == "filter"
        assert opt.is_flag is False
        assert opt.default == _UNSET_DEFAULT
        assert opt.help == FILTER_HELP

    def test_filter_param_name(self) -> None:
        assert _option(filter_option("filter_str")).name == "filter_str"

    def test_json_defaults_and_override(self) -> None:
        opt = _option(json_option())
        assert (opt.opts, opt.name, opt.is_flag, opt.help) == (
            ["--json"],
            "output_json",
            True,
            JSON_HELP,
        )
        assert _option(json_option(help_text="Other.")).help == "Other."

    def test_csv_defaults_and_override(self) -> None:
        opt = _option(csv_option())
        assert (opt.opts, opt.name, opt.is_flag, opt.help) == (
            ["--csv"],
            "output_csv",
            True,
            CSV_HELP,
        )
        over = _option(csv_option(param_name="csv_output", help_text="X"))
        assert (over.name, over.help) == ("csv_output", "X")

    def test_all_defaults_have_no_short_flag(self) -> None:
        opt = _option(all_option())
        assert (opt.opts, opt.name, opt.is_flag, opt.help) == (
            ["--all"],
            "query_all",
            True,
            ALL_HELP,
        )

    def test_all_short_flag(self) -> None:
        opt = _option(all_option(param_name="clear_all", help_text="H", short_flag=True))
        assert (opt.opts, opt.name, opt.help) == (["--all", "-a"], "clear_all", "H")


class TestParsing:
    """Tests for how the options parse on a throwaway command."""

    @pytest.mark.parametrize("flag", ["--filter", "-f"])
    def test_filter_reaches_param(self, flag: str) -> None:
        result = CliRunner().invoke(_make_cmd(filter_option("filter_str")), [flag, "{}"])
        assert result.exit_code == 0
        assert "('filter_str', '{}')" in result.output

    @pytest.mark.parametrize(
        ("factory", "flag", "name"),
        [
            (json_option, "--json", "output_json"),
            (csv_option, "--csv", "output_csv"),
            (all_option, "--all", "query_all"),
        ],
    )
    def test_flags_true_when_passed_false_when_absent(
        self, factory: Callable[[], Callable[[Any], Any]], flag: str, name: str
    ) -> None:
        cmd = _make_cmd(factory())
        assert f"('{name}', True)" in CliRunner().invoke(cmd, [flag]).output
        assert f"('{name}', False)" in CliRunner().invoke(cmd, []).output

    def test_short_a_only_with_short_flag(self) -> None:
        assert CliRunner().invoke(_make_cmd(all_option()), ["-a"]).exit_code == 2
        result = CliRunner().invoke(_make_cmd(all_option(short_flag=True)), ["-a"])
        assert result.exit_code == 0
        assert "('query_all', True)" in result.output


# (command path, option, param name, flags, is_flag, help)
_F = ("--filter", "-f")
_SITES: list[tuple[str, tuple[str, ...], str, bool, str]] = [
    ("cache check", ("--all",), "query_all", True, "Query all cached clusters."),
    ("cache check", _F, "filter_str", False, FILTER_HELP),
    ("cache check", ("--json",), "output_json", True, "Output as JSON."),
    ("cache check", ("--csv",), "output_csv", True, "Output as CSV with header row."),
    ("cache clear", ("--all", "-a"), "clear_all", True, "Clear cache for all clusters."),
    ("cache compliance", ("--all",), "query_all", True, "Check all cached clusters."),
    ("cache compliance", _F, "filter_str", False, FILTER_HELP),
    ("cache compliance", ("--json",), "output_json", True, "Output as JSON."),
    ("cache compliance", ("--csv",), "output_csv", True, "Output as CSV with header row."),
    ("cache history list", ("--json",), "output_json", True, "Output as JSON."),
    ("cache history show", ("--json",), "output_json", True, "Output as JSON."),
    ("cache history snapshot", ("--json",), "output_json", True, "Output as JSON."),
    ("cache query", _F, "filter_str", False, FILTER_HELP),
    ("cache query", ("--all",), "query_all", True, "Query all cached clusters."),
    ("cache query", ("--json",), "output_json", True, "Output as JSON."),
    ("cache query", ("--csv",), "output_csv", True, "Output as CSV with header row."),
    (
        "cache refresh",
        ("--all", "-a"),
        "refresh_all",
        True,
        "Refresh cache for all configured clusters.",
    ),
    ("cache refresh", _F, "filter_str", False, FILTER_HELP),
    ("cache schema", ("--json",), "output_json", True, "Output as JSON schema."),
    ("cache show", ("--json",), "output_json", True, "Output as JSON."),
    ("cifs session", _F, "filter", False, FILTER_HELP),
    ("events get", _F, "filter", False, FILTER_HELP),
    ("events save-azure", _F, "filter", False, FILTER_HELP),
    ("licenses check", _F, "filter", False, FILTER_HELP),
    ("licenses get", _F, "filter", False, FILTER_HELP),
    (
        "licenses get",
        ("--csv",),
        "csv_output",
        True,
        "Output to CSV file instead of console table.",
    ),
    ("licenses savings", _F, "filter", False, FILTER_HELP),
    ("metrics dump-dii", _F, "filter", False, FILTER_HELP),
    ("reports space-usage", _F, "filter", False, FILTER_HELP),
    ("reports locks", _F, "filter", False, FILTER_HELP),
    ("reports html", _F, "filter", False, FILTER_HELP),
    ("reports inventory", _F, "filter", False, FILTER_HELP),
    ("utils validate", _F, "filter", False, FILTER_HELP),
    ("utils run-cmd", _F, "filter", False, FILTER_HELP),
]


def _resolve(path: str) -> click.Command:
    cmd: click.Command = nf
    for part in path.split():
        assert isinstance(cmd, click.Group)
        found = cmd.commands[part]
        cmd = found
    return cmd


class TestDeclarationSnapshot:
    """Converted commands keep the declaration they had before the refactor."""

    @pytest.mark.parametrize(("path", "opts", "name", "is_flag", "help_text"), _SITES)
    def test_site(
        self, path: str, opts: tuple[str, ...], name: str, is_flag: bool, help_text: str
    ) -> None:
        cmd = _resolve(path)
        (opt,) = [p for p in cmd.params if isinstance(p, click.Option) and p.opts == list(opts)]
        assert opt.name == name
        assert opt.secondary_opts == []
        assert opt.is_flag is is_flag
        assert opt.multiple is False
        # Flags without an explicit default report the unset sentinel; click resolves it to False.
        assert opt.default in ((False, _UNSET_DEFAULT) if is_flag else (_UNSET_DEFAULT,))
        assert opt.type.name == ("boolean" if is_flag else "text")
        assert opt.help == help_text

    def test_cifs_csv_stays_a_path_option(self) -> None:
        (opt,) = [
            p
            for p in _resolve("cifs session").params
            if isinstance(p, click.Option) and "--csv" in p.opts
        ]
        assert opt.opts == ["--csv", "-c"]
        assert opt.name == "csv_path"
        assert isinstance(opt.type, click.Path)


class TestHelpSmoke:
    """--help still renders the shared options."""

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            (["cache", "query", "--help"], ["-f, --filter", "JSON cluster filter"]),
            (["licenses", "get", "--help"], ["-f, --filter", "JSON cluster filter"]),
            (["cache", "refresh", "--help"], ["-a, --all", "-f, --filter"]),
            (["cifs", "session", "--help"], ["-f, --filter", "-c, --csv PATH"]),
        ],
    )
    def test_help(self, args: list[str], expected: list[str]) -> None:
        result = CliRunner().invoke(nf, args)
        assert result.exit_code == 0
        for text in expected:
            assert text in result.output


def _shared_flag_hits(root: Path) -> set[tuple[str, str]]:
    """Return (relative path, flag) for each ``option(...)`` call declaring a shared flag."""
    hits: set[tuple[str, str]] = set()
    for path in sorted(root.rglob("*.py")):
        if path.name == "options.py" and path.parent == root:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            if name != "option":
                continue
            for arg in node.args:
                if isinstance(arg, ast.Constant) and arg.value in SHARED_FLAGS:
                    hits.add((path.relative_to(root).as_posix(), str(arg.value)))
    return hits


def test_no_duplicate_shared_option_declarations() -> None:
    """Test that only the allowlisted command declares a shared flag by hand."""
    assert _shared_flag_hits(CLI_DIR) == ALLOWED_LOCAL


def test_guard_detects_hand_written_options(tmp_path: Path) -> None:
    """Test that the scan catches both call forms and ignores docstrings."""
    (tmp_path / "sample.py").write_text(
        "import click\n"
        "from click import option\n"
        '@click.option("--json", "output_json", is_flag=True)\n'
        '@option("--all")\n'
        "def f() -> None:\n"
        '    """Mentions "--json" and click.option("--csv")."""\n',
        encoding="utf-8",
    )
    assert _shared_flag_hits(tmp_path) == {("sample.py", "--json"), ("sample.py", "--all")}
