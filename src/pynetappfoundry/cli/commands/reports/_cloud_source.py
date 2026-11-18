"""Pick the source of a report's cloud details: the OCCM cache or the ONTAP CLI path (#1086).

The inventory and HTML reports ask :class:`ReportCloudSource` for one cluster's cloud details.
The OCCM cache answers when it can answer the whole cluster (``occm_cloud_metadata`` returns a
complete list; AWS only, Azure and GCP always use the CLI path); otherwise the report uses
today's CLI-parsed ``entry.ontap.cloud``.  Every OCCM read goes through
``ClusterResolver``; the OCCM path makes no live call.  Console links come from the resolved
location whichever source answered the cloud fields (ADR-0033), and carry the System Manager
link of the same record (#1105).
"""

from __future__ import annotations

import logging
import sqlite3
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, Self

from pydantic import ValidationError

from pynetappfoundry.cache.cluster_resolver import ClusterResolver
from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.cache.occm_cloud_metadata import (
    CLOUD_MAPPING_PROVIDER,
    ConsoleWorkingEnvironmentLinks,
    console_links,
    occm_cloud_metadata,
    pick_occm_data,
)
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.utils.console_links import CONSOLE_UI_BASE_URL

if TYPE_CHECKING:
    from collections.abc import Sequence
    from types import TracebackType

    from pynetappfoundry.cache.cluster_resolver import OccmData
    from pynetappfoundry.core.cluster_entry import ClusterEntry
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata

logger = logging.getLogger(__name__)

_FALLBACK_ERRORS = (ValidationError, LookupError, ValueError, sqlite3.Error)


@dataclass(frozen=True)
class CloudDetails:
    """One cluster's cloud details for a report.

    Attributes:
        source: ``"occm"`` (OCCM cache), ``"cli"`` (ONTAP CLI path) or ``"none"`` (not a cloud
            cluster).
        metadata: One entry per node; empty when no source has any.
        console: The Console links, with the System Manager link from the OCCM record, or
            ``None`` when no single working environment was found.
    """

    source: Literal["occm", "cli", "none"]
    metadata: list[CloudMetadata]
    console: ConsoleWorkingEnvironmentLinks | None


class ReportCloudSource:
    """Choose OCCM or CLI cloud details per cluster.

    Args:
        resolver: The cache resolver; ``None`` means no cache is available (CLI only).
        ui_base_url: The Console UI base URL of the links.
        aws_sso_config: Optional AWS SSO settings for the instance SSO link.
    """

    def __init__(
        self,
        resolver: ClusterResolver | None,
        *,
        ui_base_url: str = CONSOLE_UI_BASE_URL,
        aws_sso_config: dict[str, str | dict[str, str]] | None = None,
    ) -> None:
        self._resolver = resolver
        self._ui_base_url = ui_base_url
        self._aws_sso_config = aws_sso_config
        self._owned: list[ClusterMetadataDB | OccmCacheDB] = []

    @classmethod
    def from_config(cls, config: Config) -> Self:
        """Open the ONTAP and OCCM cache files that exist (never create one); no AIQUM reads."""
        ontap_path = ClusterMetadataDB.default_path(config)
        occm_path = OccmCacheDB.default_path(config)
        ontap_db = ClusterMetadataDB(db_path=ontap_path) if ontap_path.exists() else None
        occm_db = OccmCacheDB(db_path=occm_path) if occm_path.exists() else None
        resolver = ClusterResolver(ontap_db=ontap_db, aiqum_db=None, occm_db=occm_db)
        ui_base_url = str(
            config.get_setting("consoleapi", "general", "ui_base_url", default=CONSOLE_UI_BASE_URL)
        )
        sso = config.settings.get("aws", {}).get("sso")
        source = cls(resolver, ui_base_url=ui_base_url, aws_sso_config=sso)
        source._owned = [db for db in (ontap_db, occm_db) if db is not None]
        return source

    def close(self) -> None:
        """Close the databases :meth:`from_config` opened."""
        for db in self._owned:
            db.close()
        self._owned = []

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def details(
        self,
        cluster_name: str,
        *,
        is_cloud: bool,
        node_names: Sequence[str],
        entry: ClusterEntry | Any,
    ) -> CloudDetails:
        """Return the cloud details of one cluster.

        Never reads ``entry.ontap.cloud`` when *is_cloud* is false: that lazy fetch falls through
        to ``virtual-machine instance show`` over SSH (#547).
        """
        picked: OccmData | None = None
        try:
            if self._resolver is not None:
                picked = pick_occm_data(self._resolver.read(cluster_name).occm)
            record = picked.record.model_dump() if picked is not None else None
            console = (
                console_links(picked.location, base_url=self._ui_base_url, record=record)
                if picked is not None
                else None
            )
            occm = self._occm_metadata(picked, record, is_cloud, node_names)
        except _FALLBACK_ERRORS as exc:
            logger.warning(
                "Cloud details of %s: OCCM cache not used (%s); using the ONTAP CLI path",
                cluster_name,
                type(exc).__name__,
            )
            console = None
            occm = None
        if occm is not None:
            return CloudDetails("occm", occm, console)
        if not is_cloud:
            return CloudDetails("none", [], console)
        ontap = entry.ontap
        cli = list(ontap.cloud) if ontap and ontap.cloud else []
        return CloudDetails("cli", cli, console)

    def _occm_metadata(
        self,
        picked: OccmData | None,
        record: dict[str, Any] | None,
        is_cloud: bool,
        node_names: Sequence[str],
    ) -> list[CloudMetadata] | None:
        """Return the adapter's answer for *picked*, or ``None`` when OCCM cannot answer."""
        if (
            picked is None
            or record is None
            or not is_cloud
            or picked.location.mapping not in CLOUD_MAPPING_PROVIDER
        ):
            return None
        return occm_cloud_metadata(
            record,
            picked.location.mapping,
            ontap_node_names=node_names,
            aws_sso_config=self._aws_sso_config,
        )
