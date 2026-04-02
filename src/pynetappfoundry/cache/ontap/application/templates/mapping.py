# ruff: noqa: E501
"""OntapApplicationTemplate type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.application.templates.model import (
    OntapApplicationTemplate,
    OntapApplicationTemplateMongoDbOnSanNewIgroup,
    OntapApplicationTemplateMongoDbOnSanSecondaryIgroup,
    OntapApplicationTemplateNasApplicationComponent,
    OntapApplicationTemplateNasCifsAccess,
    OntapApplicationTemplateNasExcludeAggregate,
    OntapApplicationTemplateNasNfsAccess,
    OntapApplicationTemplateNvmeComponent,
    OntapApplicationTemplateOracleOnNfsNfsAccess,
    OntapApplicationTemplateOracleOnSanNewIgroup,
    OntapApplicationTemplateOracleRacOnNfsNfsAccess,
    OntapApplicationTemplateOracleRacOnSanDbSid,
    OntapApplicationTemplateOracleRacOnSanNewIgroup,
    OntapApplicationTemplateS3BucketApplicationComponent,
    OntapApplicationTemplateSanApplicationComponent,
    OntapApplicationTemplateSanExcludeAggregate,
    OntapApplicationTemplateSanNewIgroup,
    OntapApplicationTemplateSqlOnSanNewIgroup,
    OntapApplicationTemplateVdiOnNasNfsAccess,
    OntapApplicationTemplateVdiOnSanNewIgroup,
    OntapApplicationTemplateVsiOnNasNfsAccess,
    OntapApplicationTemplateVsiOnSanNewIgroup,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_mongo_db_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateMongoDbOnSanNewIgroup]:
    """Transform mongo_db_on_san.new_igroups into OntapApplicationTemplateMongoDbOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "mongo_db_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationTemplateMongoDbOnSanNewIgroup(**item) for item in items]


def _transform_mongo_db_on_san_secondary_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateMongoDbOnSanSecondaryIgroup]:
    """Transform mongo_db_on_san.secondary_igroups into OntapApplicationTemplateMongoDbOnSanSecondaryIgroup list."""
    try:
        items = get_nested_value(record, "mongo_db_on_san.secondary_igroups")
    except Exception:
        items = []
    return [OntapApplicationTemplateMongoDbOnSanSecondaryIgroup(**item) for item in items]


def _transform_nas_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNasApplicationComponent]:
    """Transform nas.application_components into OntapApplicationTemplateNasApplicationComponent list."""
    try:
        items = get_nested_value(record, "nas.application_components")
    except Exception:
        items = []
    return [OntapApplicationTemplateNasApplicationComponent(**item) for item in items]


def _transform_nas_cifs_access(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNasCifsAccess]:
    """Transform nas.cifs_access into OntapApplicationTemplateNasCifsAccess list."""
    try:
        items = get_nested_value(record, "nas.cifs_access")
    except Exception:
        items = []
    return [OntapApplicationTemplateNasCifsAccess(**item) for item in items]


def _transform_nas_exclude_aggregates(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNasExcludeAggregate]:
    """Transform nas.exclude_aggregates into OntapApplicationTemplateNasExcludeAggregate list."""
    try:
        items = get_nested_value(record, "nas.exclude_aggregates")
    except Exception:
        items = []
    return [OntapApplicationTemplateNasExcludeAggregate(**item) for item in items]


def _transform_nas_nfs_access(record: dict[str, Any]) -> list[OntapApplicationTemplateNasNfsAccess]:
    """Transform nas.nfs_access into OntapApplicationTemplateNasNfsAccess list."""
    try:
        items = get_nested_value(record, "nas.nfs_access")
    except Exception:
        items = []
    return [OntapApplicationTemplateNasNfsAccess(**item) for item in items]


def _transform_nvme_components(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNvmeComponent]:
    """Transform nvme.components into OntapApplicationTemplateNvmeComponent list."""
    try:
        items = get_nested_value(record, "nvme.components")
    except Exception:
        items = []
    return [OntapApplicationTemplateNvmeComponent(**item) for item in items]


def _transform_oracle_on_nfs_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateOracleOnNfsNfsAccess]:
    """Transform oracle_on_nfs.nfs_access into OntapApplicationTemplateOracleOnNfsNfsAccess list."""
    try:
        items = get_nested_value(record, "oracle_on_nfs.nfs_access")
    except Exception:
        items = []
    return [OntapApplicationTemplateOracleOnNfsNfsAccess(**item) for item in items]


def _transform_oracle_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateOracleOnSanNewIgroup]:
    """Transform oracle_on_san.new_igroups into OntapApplicationTemplateOracleOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "oracle_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationTemplateOracleOnSanNewIgroup(**item) for item in items]


def _transform_oracle_rac_on_nfs_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateOracleRacOnNfsNfsAccess]:
    """Transform oracle_rac_on_nfs.nfs_access into OntapApplicationTemplateOracleRacOnNfsNfsAccess list."""
    try:
        items = get_nested_value(record, "oracle_rac_on_nfs.nfs_access")
    except Exception:
        items = []
    return [OntapApplicationTemplateOracleRacOnNfsNfsAccess(**item) for item in items]


def _transform_oracle_rac_on_san_db_sids(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateOracleRacOnSanDbSid]:
    """Transform oracle_rac_on_san.db_sids into OntapApplicationTemplateOracleRacOnSanDbSid list."""
    try:
        items = get_nested_value(record, "oracle_rac_on_san.db_sids")
    except Exception:
        items = []
    return [OntapApplicationTemplateOracleRacOnSanDbSid(**item) for item in items]


def _transform_oracle_rac_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateOracleRacOnSanNewIgroup]:
    """Transform oracle_rac_on_san.new_igroups into OntapApplicationTemplateOracleRacOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "oracle_rac_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationTemplateOracleRacOnSanNewIgroup(**item) for item in items]


def _transform_s3_bucket_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateS3BucketApplicationComponent]:
    """Transform s3_bucket.application_components into OntapApplicationTemplateS3BucketApplicationComponent list."""
    try:
        items = get_nested_value(record, "s3_bucket.application_components")
    except Exception:
        items = []
    return [OntapApplicationTemplateS3BucketApplicationComponent(**item) for item in items]


def _transform_san_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateSanApplicationComponent]:
    """Transform san.application_components into OntapApplicationTemplateSanApplicationComponent list."""
    try:
        items = get_nested_value(record, "san.application_components")
    except Exception:
        items = []
    return [OntapApplicationTemplateSanApplicationComponent(**item) for item in items]


def _transform_san_exclude_aggregates(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateSanExcludeAggregate]:
    """Transform san.exclude_aggregates into OntapApplicationTemplateSanExcludeAggregate list."""
    try:
        items = get_nested_value(record, "san.exclude_aggregates")
    except Exception:
        items = []
    return [OntapApplicationTemplateSanExcludeAggregate(**item) for item in items]


def _transform_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateSanNewIgroup]:
    """Transform san.new_igroups into OntapApplicationTemplateSanNewIgroup list."""
    try:
        items = get_nested_value(record, "san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationTemplateSanNewIgroup(**item) for item in items]


def _transform_sql_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateSqlOnSanNewIgroup]:
    """Transform sql_on_san.new_igroups into OntapApplicationTemplateSqlOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "sql_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationTemplateSqlOnSanNewIgroup(**item) for item in items]


def _transform_vdi_on_nas_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateVdiOnNasNfsAccess]:
    """Transform vdi_on_nas.nfs_access into OntapApplicationTemplateVdiOnNasNfsAccess list."""
    try:
        items = get_nested_value(record, "vdi_on_nas.nfs_access")
    except Exception:
        items = []
    return [OntapApplicationTemplateVdiOnNasNfsAccess(**item) for item in items]


def _transform_vdi_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateVdiOnSanNewIgroup]:
    """Transform vdi_on_san.new_igroups into OntapApplicationTemplateVdiOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "vdi_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationTemplateVdiOnSanNewIgroup(**item) for item in items]


def _transform_vsi_on_nas_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateVsiOnNasNfsAccess]:
    """Transform vsi_on_nas.nfs_access into OntapApplicationTemplateVsiOnNasNfsAccess list."""
    try:
        items = get_nested_value(record, "vsi_on_nas.nfs_access")
    except Exception:
        items = []
    return [OntapApplicationTemplateVsiOnNasNfsAccess(**item) for item in items]


def _transform_vsi_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateVsiOnSanNewIgroup]:
    """Transform vsi_on_san.new_igroups into OntapApplicationTemplateVsiOnSanNewIgroup list."""
    try:
        items = get_nested_value(record, "vsi_on_san.new_igroups")
    except Exception:
        items = []
    return [OntapApplicationTemplateVsiOnSanNewIgroup(**item) for item in items]


ONTAPAPPLICATIONTEMPLATE_MAPPING = TypeMapping(
    name="OntapApplicationTemplate",
    model_class=OntapApplicationTemplate,
    api_endpoint="/application/templates?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="description",
            api_path="description",
        ),
        FieldMapping(
            cache_attr="missing_prerequisites",
            api_path="missing_prerequisites",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.dataset.element_count",
            api_path="mongo_db_on_san.dataset.element_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.dataset.replication_factor",
            api_path="mongo_db_on_san.dataset.replication_factor",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.dataset.size",
            api_path="mongo_db_on_san.dataset.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.dataset.storage_service.name",
            api_path="mongo_db_on_san.dataset.storage_service.name",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.new_igroups",
            api_path="mongo_db_on_san.new_igroups",
            transform=_transform_mongo_db_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.os_type",
            api_path="mongo_db_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.primary_igroup_name",
            api_path="mongo_db_on_san.primary_igroup_name",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.protection_type.local_rpo",
            api_path="mongo_db_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.protection_type.remote_rpo",
            api_path="mongo_db_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san.secondary_igroups",
            api_path="mongo_db_on_san.secondary_igroups",
            transform=_transform_mongo_db_on_san_secondary_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas.application_components",
            api_path="nas.application_components",
            transform=_transform_nas_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas.cifs_access",
            api_path="nas.cifs_access",
            transform=_transform_nas_cifs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas.cifs_share_name",
            api_path="nas.cifs_share_name",
        ),
        FieldMapping(
            cache_attr="nas.exclude_aggregates",
            api_path="nas.exclude_aggregates",
            transform=_transform_nas_exclude_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas.nfs_access",
            api_path="nas.nfs_access",
            transform=_transform_nas_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas.protection_type.local_policy",
            api_path="nas.protection_type.local_policy",
        ),
        FieldMapping(
            cache_attr="nas.protection_type.local_rpo",
            api_path="nas.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="nas.protection_type.remote_rpo",
            api_path="nas.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="nvme.components",
            api_path="nvme.components",
            transform=_transform_nvme_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="nvme.os_type",
            api_path="nvme.os_type",
        ),
        FieldMapping(
            cache_attr="nvme.rpo.local.name",
            api_path="nvme.rpo.local.name",
        ),
        FieldMapping(
            cache_attr="nvme.rpo.local.policy",
            api_path="nvme.rpo.local.policy",
        ),
        FieldMapping(
            cache_attr="nvme.rpo.remote.name",
            api_path="nvme.rpo.remote.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.archive_log.size",
            api_path="oracle_on_nfs.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.archive_log.storage_service.name",
            api_path="oracle_on_nfs.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.db.size",
            api_path="oracle_on_nfs.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.db.storage_service.name",
            api_path="oracle_on_nfs.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.nfs_access",
            api_path="oracle_on_nfs.nfs_access",
            transform=_transform_oracle_on_nfs_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.ora_home.size",
            api_path="oracle_on_nfs.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.ora_home.storage_service.name",
            api_path="oracle_on_nfs.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.protection_type.local_rpo",
            api_path="oracle_on_nfs.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.protection_type.remote_rpo",
            api_path="oracle_on_nfs.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.redo_log.mirrored",
            api_path="oracle_on_nfs.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.redo_log.size",
            api_path="oracle_on_nfs.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs.redo_log.storage_service.name",
            api_path="oracle_on_nfs.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.archive_log.size",
            api_path="oracle_on_san.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san.archive_log.storage_service.name",
            api_path="oracle_on_san.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.db.size",
            api_path="oracle_on_san.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san.db.storage_service.name",
            api_path="oracle_on_san.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.igroup_name",
            api_path="oracle_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.new_igroups",
            api_path="oracle_on_san.new_igroups",
            transform=_transform_oracle_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_on_san.ora_home.size",
            api_path="oracle_on_san.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san.ora_home.storage_service.name",
            api_path="oracle_on_san.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.os_type",
            api_path="oracle_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.protection_type.local_rpo",
            api_path="oracle_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.protection_type.remote_rpo",
            api_path="oracle_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_san.redo_log.mirrored",
            api_path="oracle_on_san.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_on_san.redo_log.size",
            api_path="oracle_on_san.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san.redo_log.storage_service.name",
            api_path="oracle_on_san.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.archive_log.size",
            api_path="oracle_rac_on_nfs.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.archive_log.storage_service.name",
            api_path="oracle_rac_on_nfs.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.db.size",
            api_path="oracle_rac_on_nfs.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.db.storage_service.name",
            api_path="oracle_rac_on_nfs.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.grid_binary.size",
            api_path="oracle_rac_on_nfs.grid_binary.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.grid_binary.storage_service.name",
            api_path="oracle_rac_on_nfs.grid_binary.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.nfs_access",
            api_path="oracle_rac_on_nfs.nfs_access",
            transform=_transform_oracle_rac_on_nfs_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.ora_home.size",
            api_path="oracle_rac_on_nfs.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.ora_home.storage_service.name",
            api_path="oracle_rac_on_nfs.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.oracle_crs.copies",
            api_path="oracle_rac_on_nfs.oracle_crs.copies",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.oracle_crs.size",
            api_path="oracle_rac_on_nfs.oracle_crs.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.oracle_crs.storage_service.name",
            api_path="oracle_rac_on_nfs.oracle_crs.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.protection_type.local_rpo",
            api_path="oracle_rac_on_nfs.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.protection_type.remote_rpo",
            api_path="oracle_rac_on_nfs.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.redo_log.mirrored",
            api_path="oracle_rac_on_nfs.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.redo_log.size",
            api_path="oracle_rac_on_nfs.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs.redo_log.storage_service.name",
            api_path="oracle_rac_on_nfs.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.archive_log.size",
            api_path="oracle_rac_on_san.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.archive_log.storage_service.name",
            api_path="oracle_rac_on_san.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.db.size",
            api_path="oracle_rac_on_san.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.db.storage_service.name",
            api_path="oracle_rac_on_san.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.db_sids",
            api_path="oracle_rac_on_san.db_sids",
            transform=_transform_oracle_rac_on_san_db_sids,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.grid_binary.size",
            api_path="oracle_rac_on_san.grid_binary.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.grid_binary.storage_service.name",
            api_path="oracle_rac_on_san.grid_binary.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.new_igroups",
            api_path="oracle_rac_on_san.new_igroups",
            transform=_transform_oracle_rac_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.ora_home.size",
            api_path="oracle_rac_on_san.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.ora_home.storage_service.name",
            api_path="oracle_rac_on_san.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.oracle_crs.copies",
            api_path="oracle_rac_on_san.oracle_crs.copies",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.oracle_crs.size",
            api_path="oracle_rac_on_san.oracle_crs.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.oracle_crs.storage_service.name",
            api_path="oracle_rac_on_san.oracle_crs.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.os_type",
            api_path="oracle_rac_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.protection_type.local_rpo",
            api_path="oracle_rac_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.protection_type.remote_rpo",
            api_path="oracle_rac_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.redo_log.mirrored",
            api_path="oracle_rac_on_san.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.redo_log.size",
            api_path="oracle_rac_on_san.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san.redo_log.storage_service.name",
            api_path="oracle_rac_on_san.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="protocol",
            api_path="protocol",
        ),
        FieldMapping(
            cache_attr="s3_bucket.application_components",
            api_path="s3_bucket.application_components",
            transform=_transform_s3_bucket_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="s3_bucket.protection_type.remote_rpo",
            api_path="s3_bucket.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="san.application_components",
            api_path="san.application_components",
            transform=_transform_san_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="san.exclude_aggregates",
            api_path="san.exclude_aggregates",
            transform=_transform_san_exclude_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="san.new_igroups",
            api_path="san.new_igroups",
            transform=_transform_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="san.os_type",
            api_path="san.os_type",
        ),
        FieldMapping(
            cache_attr="san.protection_type.local_policy",
            api_path="san.protection_type.local_policy",
        ),
        FieldMapping(
            cache_attr="san.protection_type.local_rpo",
            api_path="san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="san.protection_type.remote_rpo",
            api_path="san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_san.db.size",
            api_path="sql_on_san.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san.db.storage_service.name",
            api_path="sql_on_san.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_san.igroup_name",
            api_path="sql_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="sql_on_san.log.size",
            api_path="sql_on_san.log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san.log.storage_service.name",
            api_path="sql_on_san.log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_san.new_igroups",
            api_path="sql_on_san.new_igroups",
            transform=_transform_sql_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="sql_on_san.os_type",
            api_path="sql_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="sql_on_san.protection_type.local_rpo",
            api_path="sql_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_san.protection_type.remote_rpo",
            api_path="sql_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_san.server_cores_count",
            api_path="sql_on_san.server_cores_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san.temp_db.size",
            api_path="sql_on_san.temp_db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san.temp_db.storage_service.name",
            api_path="sql_on_san.temp_db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.access.installer",
            api_path="sql_on_smb.access.installer",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.access.service_account",
            api_path="sql_on_smb.access.service_account",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.db.size",
            api_path="sql_on_smb.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb.db.storage_service.name",
            api_path="sql_on_smb.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.log.size",
            api_path="sql_on_smb.log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb.log.storage_service.name",
            api_path="sql_on_smb.log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.protection_type.local_rpo",
            api_path="sql_on_smb.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.protection_type.remote_rpo",
            api_path="sql_on_smb.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_smb.server_cores_count",
            api_path="sql_on_smb.server_cores_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb.temp_db.size",
            api_path="sql_on_smb.temp_db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb.temp_db.storage_service.name",
            api_path="sql_on_smb.temp_db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.desktops.count",
            api_path="vdi_on_nas.desktops.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.desktops.size",
            api_path="vdi_on_nas.desktops.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.desktops.storage_service.name",
            api_path="vdi_on_nas.desktops.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.hyper_v_access.service_account",
            api_path="vdi_on_nas.hyper_v_access.service_account",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.nfs_access",
            api_path="vdi_on_nas.nfs_access",
            transform=_transform_vdi_on_nas_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.protection_type.local_rpo",
            api_path="vdi_on_nas.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas.protection_type.remote_rpo",
            api_path="vdi_on_nas.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="vdi_on_san.desktops.count",
            api_path="vdi_on_san.desktops.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_san.desktops.size",
            api_path="vdi_on_san.desktops.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_san.desktops.storage_service.name",
            api_path="vdi_on_san.desktops.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vdi_on_san.hypervisor",
            api_path="vdi_on_san.hypervisor",
        ),
        FieldMapping(
            cache_attr="vdi_on_san.igroup_name",
            api_path="vdi_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="vdi_on_san.new_igroups",
            api_path="vdi_on_san.new_igroups",
            transform=_transform_vdi_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="vdi_on_san.protection_type.local_rpo",
            api_path="vdi_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vdi_on_san.protection_type.remote_rpo",
            api_path="vdi_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.datastore.count",
            api_path="vsi_on_nas.datastore.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.datastore.size",
            api_path="vsi_on_nas.datastore.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.datastore.storage_service.name",
            api_path="vsi_on_nas.datastore.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.hyper_v_access.service_account",
            api_path="vsi_on_nas.hyper_v_access.service_account",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.nfs_access",
            api_path="vsi_on_nas.nfs_access",
            transform=_transform_vsi_on_nas_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.protection_type.local_rpo",
            api_path="vsi_on_nas.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas.protection_type.remote_rpo",
            api_path="vsi_on_nas.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_san.datastore.count",
            api_path="vsi_on_san.datastore.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_san.datastore.size",
            api_path="vsi_on_san.datastore.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_san.datastore.storage_service.name",
            api_path="vsi_on_san.datastore.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vsi_on_san.hypervisor",
            api_path="vsi_on_san.hypervisor",
        ),
        FieldMapping(
            cache_attr="vsi_on_san.igroup_name",
            api_path="vsi_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="vsi_on_san.new_igroups",
            api_path="vsi_on_san.new_igroups",
            transform=_transform_vsi_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="vsi_on_san.protection_type.local_rpo",
            api_path="vsi_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_san.protection_type.remote_rpo",
            api_path="vsi_on_san.protection_type.remote_rpo",
        ),
    ),
)

model_registry.register_mapping("OntapApplicationTemplate", ONTAPAPPLICATIONTEMPLATE_MAPPING)
