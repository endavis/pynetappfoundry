"""Tests for CLI decorators."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import click
from click.testing import CliRunner

from pynetappfoundry.cli.decorators import with_config


class TestWithConfigScriptName:
    """Tests for script_name derivation from command path."""

    def _make_cli(self) -> click.Group:
        """Build a test CLI with nested commands."""

        @click.group()
        @click.pass_context
        def nf(ctx: click.Context) -> None:
            ctx.ensure_object(dict)
            ctx.obj["config_dir"] = "config"
            ctx.obj["output_dir"] = ""
            ctx.obj["debug"] = False

        @nf.group()
        def licenses() -> None:
            pass

        @licenses.command()
        @with_config("test failed")
        def get(config: object, clusters: object) -> None:
            # Echo the script_name so we can verify it
            click.echo(config.script_name)  # type: ignore[union-attr]

        @nf.group()
        def events() -> None:
            pass

        @events.command()
        @with_config("test failed")
        def get2(config: object, clusters: object) -> None:
            click.echo(config.script_name)  # type: ignore[union-attr]

        # Register get2 as "get" in events group
        events.add_command(get2, "get")

        return nf

    @patch("pynetappfoundry.cli.decorators.Config")
    def test_licenses_get_script_name(self, mock_config_cls: MagicMock) -> None:
        """Test that 'nf licenses get' produces script_name 'licenses_get'."""
        mock_config = MagicMock()
        mock_config.script_name = ""
        mock_config_cls.return_value = mock_config
        mock_config_cls.return_value.get_clusters.return_value = {}

        # Capture the script_name passed to Config
        def capture_config(*args: object, **kwargs: object) -> MagicMock:
            mock_config.script_name = kwargs.get("script_name", "")
            mock_config.get_clusters = MagicMock(return_value={})
            return mock_config

        mock_config_cls.side_effect = capture_config

        runner = CliRunner()
        cli = self._make_cli()
        result = runner.invoke(cli, ["licenses", "get"])

        assert result.exit_code == 0
        assert mock_config.script_name == "licenses_get"

    @patch("pynetappfoundry.cli.decorators.Config")
    def test_events_get_script_name(self, mock_config_cls: MagicMock) -> None:
        """Test that 'nf events get' produces script_name 'events_get'."""
        mock_config = MagicMock()
        mock_config_cls.return_value = mock_config

        def capture_config(*args: object, **kwargs: object) -> MagicMock:
            mock_config.script_name = kwargs.get("script_name", "")
            mock_config.get_clusters = MagicMock(return_value={})
            return mock_config

        mock_config_cls.side_effect = capture_config

        runner = CliRunner()
        cli = self._make_cli()
        result = runner.invoke(cli, ["events", "get"])

        assert result.exit_code == 0
        assert mock_config.script_name == "events_get"
