"""Shared state declarations and helpers for the collector mixins (#899).

``MetadataCollector`` (``cache/collector.py``) is assembled from mixins that
live in sibling ``_collector_*`` modules.  The mixins share instance state set
up by ``MetadataCollector.__init__``; this module declares that state (types
only, no ``__init__``) so mypy can check each mixin on its own.
"""

from __future__ import annotations

import logging
import threading
from concurrent.futures import Future
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pynetappfoundry.cache._collector_cli import SshPreconnect
    from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
    from pynetappfoundry.clients.ontap.cli import ONTAPCLI

# One logger name for every collector module, so log filtering by
# ``pynetappfoundry.cache.collector`` keeps working after the split.
logger = logging.getLogger("pynetappfoundry.cache.collector")


class _CollectorState:
    """Instance attributes shared by the collector mixins (annotations only)."""

    api_client: ONTAPAPIClient | None
    cli_client: ONTAPCLI | None
    aws_sso_config: dict[str, str | dict[str, str]] | None
    parallel: bool
    max_workers: int
    _cluster_name: str
    _api_cache: dict[str, Any]
    _inflight: dict[str, Future[Any]]
    _cache_lock: threading.Lock
    _results_cache: dict[str, Any]
    _ssh_preconnect: SshPreconnect | None

    @property
    def _log_prefix(self) -> str:
        """Return log prefix with cluster name for consistent logging."""
        if self._cluster_name:
            return f"[{self._cluster_name}:collector]"
        return "[collector]"

    def _log_missing_fields(
        self,
        record: dict[str, Any],
        expected_fields: list[str],
        record_type: str,
        record_id: str,
    ) -> None:
        """Log error messages for expected API fields missing from a record.

        Only logs when a key is absent from the dict — not when present
        with a null, empty, or zero value.

        Args:
            record: The API response record dict.
            expected_fields: Top-level keys expected in the record.
            record_type: Human-readable type (e.g., "Volume", "Aggregate").
            record_id: Identifier for the record (name or uuid).
        """
        for field in expected_fields:
            if field not in record:
                logger.error(
                    "%s MISSING_FIELD: %s '%s' - '%s' not in API response",
                    self._log_prefix,
                    record_type,
                    record_id,
                    field,
                )
