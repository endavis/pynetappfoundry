"""Tests for cache history CLI rendering."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from pynetappfoundry.cli.main import nf


def _config_dir(tmp_path: Path) -> Path:
    """Create a minimal config directory."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "settings.toml").write_text(
        '[ontapapi]\n[ontapapi.general]\nbase_api_path = "/api"\n'
    )
    return config_dir


class TestShowDiffMarkup:
    """Cached values containing Rich markup must render literally."""

    @patch("pynetappfoundry.cli.commands.cache.history.CacheHistoryDB")
    def test_markup_in_values_is_rendered_literally(
        self, mock_db_class: MagicMock, tmp_path: Path
    ) -> None:
        """Brackets in category, entity, field, old and new values do not break rendering."""
        summary: list[dict[str, object]] = [
            {"type": "added", "category": "cat[/x]", "entity": "ent[b]"},
            {"type": "removed", "category": "cat[/x]", "entity": "ent[b]"},
            {
                "type": "modified",
                "category": "cat[/x]",
                "entity": "ent[b]",
                "field": "fld[/x]",
                "old": "old[b]",
                "new": "new[/x]",
            },
        ]
        mock_db_class.return_value.get_change_by_id.return_value = {
            "id": 1,
            "cluster_name": "c[/x]",
            "changed_at": "2025-01-01T00:00:00",
            "summary": summary,
        }

        result = CliRunner().invoke(
            nf, ["-c", str(_config_dir(tmp_path)), "cache", "history", "diff", "1"]
        )

        assert result.exception is None or isinstance(result.exception, SystemExit)
        assert "cat[/x]: ent[b]" in result.output
        assert "fld[/x]: old[b] -> new[/x]" in result.output
