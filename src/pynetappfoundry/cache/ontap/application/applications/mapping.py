# ruff: noqa: E501
"""OntapApplication type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.application.applications.model import (
    OntapApplication,
    OntapApplicationMongoDbOnSanNewIgroup,
    OntapApplicationMongoDbOnSanSecondaryIgroup,
    OntapApplicationNasApplicationComponent,
    OntapApplicationNasCifsAccess,
    OntapApplicationNasExcludeAggregate,
    OntapApplicationNasNfsAccess,
    OntapApplicationNvmeComponent,
    OntapApplicationOracleOnNfsNfsAccess,
    OntapApplicationOracleOnSanNewIgroup,
    OntapApplicationOracleRacOnNfsNfsAccess,
    OntapApplicationOracleRacOnSanDbSid,
    OntapApplicationOracleRacOnSanNewIgroup,
    OntapApplicationRpoComponent,
    OntapApplicationS3BucketApplicationComponent,
    OntapApplicationSanApplicationComponent,
    OntapApplicationSanExcludeAggregate,
    OntapApplicationSanNewIgroup,
    OntapApplicationSqlOnSanNewIgroup,
    OntapApplicationStatisticsComponent,
    OntapApplicationVdiOnNasNfsAccess,
    OntapApplicationVdiOnSanNewIgroup,
    OntapApplicationVsiOnNasNfsAccess,
    OntapApplicationVsiOnSanNewIgroup,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_rpo_components(record: dict[str, Any]) -> list[OntapApplicationRpoComponent]:
    """Transform rpo.components into OntapApplicationRpoComponent list."""
    try:
        items = get_nested_value(record, "rpo.components")
    except Exception:
        items = []
    return [OntapApplicationRpoComponent(**item) for item in items]


def _transform_statistics_components(
    record: dict[str, Any],
) -> list[OntapApplicationStatisticsComponent]:
    """Transform statistics.components into OntapApplicationStatisticsComponent list."""
    try:
        items = get_nested_value(record, "statistics.components")
    except Exception:
        items = []
    return [OntapApplicationStatisticsComponent(**item) for item in items]


def _transform_mongo_db_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationMongoDbOnSanNewIgroup]:
    """Transform mongo_db_on_san.new_igroups into OntapApplicationMongoDbOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "mongo_db_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationMongoDbOnSanNewIgroup(**item) for item in items]


def _transform_mongo_db_on_san_secondary_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationMongoDbOnSanSecondaryIgroup]:
    """Transform mongo_db_on_san.secondary_igroups into OntapApplicationMongoDbOnSanSecondaryIgroup list."""
    try:
        items = get_nested_value(record, "mongo_db_on_san.secondary_igroups")
    except Exception:
        items = []
    return [OntapApplicationMongoDbOnSanSecondaryIgroup(**item) for item in items]


def _transform_nas_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationNasApplicationComponent]:
    """Transform nas.application_components into OntapApplicationNasApplicationComponent list."""
    try:
        items = get_nested_value(record, "nas.application_components")
    except Exception:
        items = []
    return [OntapApplicationNasApplicationComponent(**item) for item in items]


def _transform_nas_cifs_access(record: dict[str, Any]) -> list[OntapApplicationNasCifsAccess]:
    """Transform nas.cifs_access into OntapApplicationNasCifsAccess list."""
    try:
        items = get_nested_value(record, "nas.cifs_access")
    except Exception:
        items = []
    return [OntapApplicationNasCifsAccess(**item) for item in items]


def _transform_nas_exclude_aggregates(
    record: dict[str, Any],
) -> list[OntapApplicationNasExcludeAggregate]:
    """Transform nas.exclude_aggregates into OntapApplicationNasExcludeAggregate list."""
    try:
        items = get_nested_value(record, "nas.exclude_aggregates")
    except Exception:
        items = []
    return [OntapApplicationNasExcludeAggregate(**item) for item in items]


def _transform_nas_nfs_access(record: dict[str, Any]) -> list[OntapApplicationNasNfsAccess]:
    """Transform nas.nfs_access into OntapApplicationNasNfsAccess list."""
    try:
        items = get_nested_value(record, "nas.nfs_access")
    except Exception:
        items = []
    return [OntapApplicationNasNfsAccess(**item) for item in items]


def _transform_nvme_components(record: dict[str, Any]) -> list[OntapApplicationNvmeComponent]:
    """Transform nvme.components into OntapApplicationNvmeComponent list."""
    try:
        items = get_nested_value(record, "nvme.components")
    except Exception:
        items = []
    return [OntapApplicationNvmeComponent(**item) for item in items]


def _transform_oracle_on_nfs_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationOracleOnNfsNfsAccess]:
    """Transform oracle_on_nfs.nfs_access into OntapApplicationOracleOnNfsNfsAccess list."""
    try:
        items = get_nested_value(record, "oracle_on_nfs.nfs_access")
    except Exception:
        items = []
    return [OntapApplicationOracleOnNfsNfsAccess(**item) for item in items]


def _transform_oracle_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationOracleOnSanNewIgroup]:
    """Transform oracle_on_san.new_igroups into OntapApplicationOracleOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "oracle_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationOracleOnSanNewIgroup(**item) for item in items]


def _transform_oracle_rac_on_nfs_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationOracleRacOnNfsNfsAccess]:
    """Transform oracle_rac_on_nfs.nfs_access into OntapApplicationOracleRacOnNfsNfsAccess list."""
    try:
        items = get_nested_value(record, "oracle_rac_on_nfs.nfs_access")
    except Exception:
        items = []
    return [OntapApplicationOracleRacOnNfsNfsAccess(**item) for item in items]


def _transform_oracle_rac_on_san_db_sids(
    record: dict[str, Any],
) -> list[OntapApplicationOracleRacOnSanDbSid]:
    """Transform oracle_rac_on_san.db_sids into OntapApplicationOracleRacOnSanDbSid list."""
    try:
        items = get_nested_value(record, "oracle_rac_on_san.db_sids")
    except Exception:
        items = []
    return [OntapApplicationOracleRacOnSanDbSid(**item) for item in items]


def _transform_oracle_rac_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationOracleRacOnSanNewIgroup]:
    """Transform oracle_rac_on_san.new_igroups into OntapApplicationOracleRacOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "oracle_rac_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationOracleRacOnSanNewIgroup(**item) for item in items]


def _transform_s3_bucket_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationS3BucketApplicationComponent]:
    """Transform s3_bucket.application_components into OntapApplicationS3BucketApplicationComponent list."""
    try:
        items = get_nested_value(record, "s3_bucket.application_components")
    except Exception:
        items = []
    return [OntapApplicationS3BucketApplicationComponent(**item) for item in items]


def _transform_san_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationSanApplicationComponent]:
    """Transform san.application_components into OntapApplicationSanApplicationComponent list."""
    try:
        items = get_nested_value(record, "san.application_components")
    except Exception:
        items = []
    return [OntapApplicationSanApplicationComponent(**item) for item in items]


def _transform_san_exclude_aggregates(
    record: dict[str, Any],
) -> list[OntapApplicationSanExcludeAggregate]:
    """Transform san.exclude_aggregates into OntapApplicationSanExcludeAggregate list."""
    try:
        items = get_nested_value(record, "san.exclude_aggregates")
    except Exception:
        items = []
    return [OntapApplicationSanExcludeAggregate(**item) for item in items]


def _transform_san_new_igroups(record: dict[str, Any]) -> list[OntapApplicationSanNewIgroup]:
    """Transform san.new_igroups into OntapApplicationSanNewIgroup list."""
    try:
        items = get_nested_value(record, "san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationSanNewIgroup(**item) for item in items]


def _transform_sql_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationSqlOnSanNewIgroup]:
    """Transform sql_on_san.new_igroups into OntapApplicationSqlOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "sql_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationSqlOnSanNewIgroup(**item) for item in items]


def _transform_vdi_on_nas_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationVdiOnNasNfsAccess]:
    """Transform vdi_on_nas.nfs_access into OntapApplicationVdiOnNasNfsAccess list."""
    try:
        items = get_nested_value(record, "vdi_on_nas.nfs_access")
    except Exception:
        items = []
    return [OntapApplicationVdiOnNasNfsAccess(**item) for item in items]


def _transform_vdi_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationVdiOnSanNewIgroup]:
    """Transform vdi_on_san.new_igroups into OntapApplicationVdiOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "vdi_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationVdiOnSanNewIgroup(**item) for item in items]


def _transform_vsi_on_nas_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationVsiOnNasNfsAccess]:
    """Transform vsi_on_nas.nfs_access into OntapApplicationVsiOnNasNfsAccess list."""
    try:
        items = get_nested_value(record, "vsi_on_nas.nfs_access")
    except Exception:
        items = []
    return [OntapApplicationVsiOnNasNfsAccess(**item) for item in items]


def _transform_vsi_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationVsiOnSanNewIgroup]:
    """Transform vsi_on_san.new_igroups into OntapApplicationVsiOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "vsi_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationVsiOnSanNewIgroup(**item) for item in items]


ONTAPAPPLICATION_MAPPING = TypeMapping(
    name="OntapApplication",
    model_class=OntapApplication,
    api_endpoint="/application/applications?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="creation_timestamp",
        ),
        FieldMapping(
            cache_attr="delete_data",
            default=False,
        ),
        FieldMapping(
            cache_attr="generation",
            default=0,
        ),
        FieldMapping(
            cache_attr="protection_granularity",
        ),
        FieldMapping(
            cache_attr="rpo.components",
            transform=_transform_rpo_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="rpo.is_supported",
            default=False,
        ),
        FieldMapping(
            cache_attr="rpo.local.name",
        ),
        FieldMapping(
            cache_attr="rpo.local.description",
        ),
        FieldMapping(
            cache_attr="rpo.remote.name",
        ),
        FieldMapping(
            cache_attr="rpo.remote.description",
        ),
        FieldMapping(
            cache_attr="smart_container",
            default=False,
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="statistics.components",
            cache_strategy="realtime",
            transform=_transform_statistics_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="statistics.iops.per_tb",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.iops.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.latency.average",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.latency.raw",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.shared_storage_pool",
            cache_strategy="realtime",
            default=False,
        ),
        FieldMapping(
            cache_attr="statistics.snapshot.reserve",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.snapshot.used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.space.available",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.space.logical_used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.space.provisioned",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.space.reserved_unused",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.space.savings",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.space.used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.space.used_excluding_reserves",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.space.used_percent",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.statistics_incomplete",
            cache_strategy="realtime",
            default=False,
        ),
        FieldMapping(
            cache_attr="template.name",
        ),
        FieldMapping(
            cache_attr="template.protocol",
        ),
        FieldMapping(
            cache_attr="template.version",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.dataset.element_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.dataset.replication_factor",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.dataset.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.dataset.storage_service.name",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.new_igroups",
            transform=_transform_mongo_db_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.primary_igroup_name",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.secondary_igroups",
            transform=_transform_mongo_db_on_san_secondary_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas.application_components",
            transform=_transform_nas_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas.cifs_access",
            transform=_transform_nas_cifs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas.cifs_share_name",
        ),
        FieldMapping(
            cache_attr="nas.exclude_aggregates",
            transform=_transform_nas_exclude_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas.nfs_access",
            transform=_transform_nas_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas.protection_type.local_policy",
        ),
        FieldMapping(
            cache_attr="nas.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="nas.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="nvme.components",
            transform=_transform_nvme_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="nvme.os_type",
        ),
        FieldMapping(
            cache_attr="nvme.rpo.local.name",
        ),
        FieldMapping(
            cache_attr="nvme.rpo.local.policy",
        ),
        FieldMapping(
            cache_attr="nvme.rpo.remote.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.nfs_access",
            transform=_transform_oracle_on_nfs_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.new_igroups",
            transform=_transform_oracle_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_on_san.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_on_san.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.grid_binary.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.grid_binary.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.nfs_access",
            transform=_transform_oracle_rac_on_nfs_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.oracle_crs.copies",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.oracle_crs.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.oracle_crs.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.db_sids",
            transform=_transform_oracle_rac_on_san_db_sids,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.grid_binary.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.grid_binary.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.new_igroups",
            transform=_transform_oracle_rac_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.oracle_crs.copies",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.oracle_crs.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.oracle_crs.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="s3_bucket.application_components",
            transform=_transform_s3_bucket_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="s3_bucket.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="san.application_components",
            transform=_transform_san_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="san.exclude_aggregates",
            transform=_transform_san_exclude_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="san.new_igroups",
            transform=_transform_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="san.os_type",
        ),
        FieldMapping(
            cache_attr="san.protection_type.local_policy",
        ),
        FieldMapping(
            cache_attr="san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_san.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="sql_on_san.log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san.log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_san.new_igroups",
            transform=_transform_sql_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="sql_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="sql_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_san.server_cores_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san.temp_db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san.temp_db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.access.installer",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.access.service_account",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb.log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.server_cores_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb.temp_db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb.temp_db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.desktops.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.desktops.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.desktops.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.hyper_v_access.service_account",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.nfs_access",
            transform=_transform_vdi_on_nas_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="vdi_on_san.desktops.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_san.desktops.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_san.desktops.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vdi_on_san.hypervisor",
        ),
        FieldMapping(
            cache_attr="vdi_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="vdi_on_san.new_igroups",
            transform=_transform_vdi_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="vdi_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vdi_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.datastore.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.datastore.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.datastore.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.hyper_v_access.service_account",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.nfs_access",
            transform=_transform_vsi_on_nas_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_san.datastore.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_san.datastore.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_san.datastore.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vsi_on_san.hypervisor",
        ),
        FieldMapping(
            cache_attr="vsi_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="vsi_on_san.new_igroups",
            transform=_transform_vsi_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="vsi_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_san.protection_type.remote_rpo",
        ),
    ),
)

model_registry.register_mapping("OntapApplication", ONTAPAPPLICATION_MAPPING)
