# ruff: noqa: E501
"""OntapApplication type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.application.applications.model import (
    OntapApplication,
    OntapApplicationApplicationComponent,
    OntapApplicationApplicationComponent2,
    OntapApplicationApplicationComponent3,
    OntapApplicationCifsAccess,
    OntapApplicationComponent,
    OntapApplicationComponent2,
    OntapApplicationComponent3,
    OntapApplicationDbSid,
    OntapApplicationExcludeAggregate,
    OntapApplicationExcludeAggregate2,
    OntapApplicationNewIgroup,
    OntapApplicationNewIgroup2,
    OntapApplicationNewIgroup3,
    OntapApplicationNewIgroup4,
    OntapApplicationNewIgroup5,
    OntapApplicationNewIgroup6,
    OntapApplicationNewIgroup7,
    OntapApplicationNfsAccess,
    OntapApplicationNfsAccess2,
    OntapApplicationNfsAccess3,
    OntapApplicationNfsAccess4,
    OntapApplicationNfsAccess5,
    OntapApplicationSecondaryIgroup,
)


def _transform_rpo_components(record: dict[str, Any]) -> list[OntapApplicationComponent]:
    """Transform rpo.components into OntapApplicationComponent list."""
    return [OntapApplicationComponent(**item) for item in record.get("rpo.components", [])]


def _transform_statistics_components(record: dict[str, Any]) -> list[OntapApplicationComponent2]:
    """Transform statistics.components into OntapApplicationComponent2 list."""
    return [OntapApplicationComponent2(**item) for item in record.get("statistics.components", [])]


def _transform_mongo_db_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationNewIgroup]:
    """Transform mongo_db_on_san.new_igroups into OntapApplicationNewIgroup list."""
    return [
        OntapApplicationNewIgroup(**item) for item in record.get("mongo_db_on_san.new_igroups", [])
    ]


def _transform_mongo_db_on_san_secondary_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationSecondaryIgroup]:
    """Transform mongo_db_on_san.secondary_igroups into OntapApplicationSecondaryIgroup list."""
    return [
        OntapApplicationSecondaryIgroup(**item)
        for item in record.get("mongo_db_on_san.secondary_igroups", [])
    ]


def _transform_nas_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationApplicationComponent]:
    """Transform nas.application_components into OntapApplicationApplicationComponent list."""
    return [
        OntapApplicationApplicationComponent(**item)
        for item in record.get("nas.application_components", [])
    ]


def _transform_nas_cifs_access(record: dict[str, Any]) -> list[OntapApplicationCifsAccess]:
    """Transform nas.cifs_access into OntapApplicationCifsAccess list."""
    return [OntapApplicationCifsAccess(**item) for item in record.get("nas.cifs_access", [])]


def _transform_nas_exclude_aggregates(
    record: dict[str, Any],
) -> list[OntapApplicationExcludeAggregate]:
    """Transform nas.exclude_aggregates into OntapApplicationExcludeAggregate list."""
    return [
        OntapApplicationExcludeAggregate(**item)
        for item in record.get("nas.exclude_aggregates", [])
    ]


def _transform_nas_nfs_access(record: dict[str, Any]) -> list[OntapApplicationNfsAccess]:
    """Transform nas.nfs_access into OntapApplicationNfsAccess list."""
    return [OntapApplicationNfsAccess(**item) for item in record.get("nas.nfs_access", [])]


def _transform_nvme_components(record: dict[str, Any]) -> list[OntapApplicationComponent3]:
    """Transform nvme.components into OntapApplicationComponent3 list."""
    return [OntapApplicationComponent3(**item) for item in record.get("nvme.components", [])]


def _transform_oracle_on_nfs_nfs_access(record: dict[str, Any]) -> list[OntapApplicationNfsAccess2]:
    """Transform oracle_on_nfs.nfs_access into OntapApplicationNfsAccess2 list."""
    return [
        OntapApplicationNfsAccess2(**item) for item in record.get("oracle_on_nfs.nfs_access", [])
    ]


def _transform_oracle_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationNewIgroup2]:
    """Transform oracle_on_san.new_igroups into OntapApplicationNewIgroup2 list."""
    return [
        OntapApplicationNewIgroup2(**item) for item in record.get("oracle_on_san.new_igroups", [])
    ]


def _transform_oracle_rac_on_nfs_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationNfsAccess3]:
    """Transform oracle_rac_on_nfs.nfs_access into OntapApplicationNfsAccess3 list."""
    return [
        OntapApplicationNfsAccess3(**item)
        for item in record.get("oracle_rac_on_nfs.nfs_access", [])
    ]


def _transform_oracle_rac_on_san_db_sids(record: dict[str, Any]) -> list[OntapApplicationDbSid]:
    """Transform oracle_rac_on_san.db_sids into OntapApplicationDbSid list."""
    return [OntapApplicationDbSid(**item) for item in record.get("oracle_rac_on_san.db_sids", [])]


def _transform_oracle_rac_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationNewIgroup3]:
    """Transform oracle_rac_on_san.new_igroups into OntapApplicationNewIgroup3 list."""
    return [
        OntapApplicationNewIgroup3(**item)
        for item in record.get("oracle_rac_on_san.new_igroups", [])
    ]


def _transform_s3_bucket_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationApplicationComponent2]:
    """Transform s3_bucket.application_components into OntapApplicationApplicationComponent2 list."""
    return [
        OntapApplicationApplicationComponent2(**item)
        for item in record.get("s3_bucket.application_components", [])
    ]


def _transform_san_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationApplicationComponent3]:
    """Transform san.application_components into OntapApplicationApplicationComponent3 list."""
    return [
        OntapApplicationApplicationComponent3(**item)
        for item in record.get("san.application_components", [])
    ]


def _transform_san_exclude_aggregates(
    record: dict[str, Any],
) -> list[OntapApplicationExcludeAggregate2]:
    """Transform san.exclude_aggregates into OntapApplicationExcludeAggregate2 list."""
    return [
        OntapApplicationExcludeAggregate2(**item)
        for item in record.get("san.exclude_aggregates", [])
    ]


def _transform_san_new_igroups(record: dict[str, Any]) -> list[OntapApplicationNewIgroup4]:
    """Transform san.new_igroups into OntapApplicationNewIgroup4 list."""
    return [OntapApplicationNewIgroup4(**item) for item in record.get("san.new_igroups", [])]


def _transform_sql_on_san_new_igroups(record: dict[str, Any]) -> list[OntapApplicationNewIgroup5]:
    """Transform sql_on_san.new_igroups into OntapApplicationNewIgroup5 list."""
    return [OntapApplicationNewIgroup5(**item) for item in record.get("sql_on_san.new_igroups", [])]


def _transform_vdi_on_nas_nfs_access(record: dict[str, Any]) -> list[OntapApplicationNfsAccess4]:
    """Transform vdi_on_nas.nfs_access into OntapApplicationNfsAccess4 list."""
    return [OntapApplicationNfsAccess4(**item) for item in record.get("vdi_on_nas.nfs_access", [])]


def _transform_vdi_on_san_new_igroups(record: dict[str, Any]) -> list[OntapApplicationNewIgroup6]:
    """Transform vdi_on_san.new_igroups into OntapApplicationNewIgroup6 list."""
    return [OntapApplicationNewIgroup6(**item) for item in record.get("vdi_on_san.new_igroups", [])]


def _transform_vsi_on_nas_nfs_access(record: dict[str, Any]) -> list[OntapApplicationNfsAccess5]:
    """Transform vsi_on_nas.nfs_access into OntapApplicationNfsAccess5 list."""
    return [OntapApplicationNfsAccess5(**item) for item in record.get("vsi_on_nas.nfs_access", [])]


def _transform_vsi_on_san_new_igroups(record: dict[str, Any]) -> list[OntapApplicationNewIgroup7]:
    """Transform vsi_on_san.new_igroups into OntapApplicationNewIgroup7 list."""
    return [OntapApplicationNewIgroup7(**item) for item in record.get("vsi_on_san.new_igroups", [])]


ONTAPAPPLICATION_MAPPING = TypeMapping(
    name="OntapApplication",
    model_class=OntapApplication,
    api_endpoint="/application/applications?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="creation_timestamp",
            api_path="creation_timestamp",
        ),
        FieldMapping(
            cache_attr="delete_data",
            api_path="delete_data",
            default=False,
        ),
        FieldMapping(
            cache_attr="generation",
            api_path="generation",
            default=0,
        ),
        FieldMapping(
            cache_attr="protection_granularity",
            api_path="protection_granularity",
        ),
        FieldMapping(
            cache_attr="rpo_components",
            transform=_transform_rpo_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="rpo_is_supported",
            api_path="rpo.is_supported",
            default=False,
        ),
        FieldMapping(
            cache_attr="rpo_local_name",
            api_path="rpo.local.name",
        ),
        FieldMapping(
            cache_attr="rpo_local_description",
            api_path="rpo.local.description",
        ),
        FieldMapping(
            cache_attr="rpo_remote_name",
            api_path="rpo.remote.name",
        ),
        FieldMapping(
            cache_attr="rpo_remote_description",
            api_path="rpo.remote.description",
        ),
        FieldMapping(
            cache_attr="smart_container",
            api_path="smart_container",
            default=False,
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="statistics_components",
            transform=_transform_statistics_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="statistics_iops_per_tb",
            api_path="statistics.iops.per_tb",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_iops_total",
            api_path="statistics.iops.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_latency_average",
            api_path="statistics.latency.average",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_latency_raw",
            api_path="statistics.latency.raw",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_shared_storage_pool",
            api_path="statistics.shared_storage_pool",
            default=False,
        ),
        FieldMapping(
            cache_attr="statistics_snapshot_reserve",
            api_path="statistics.snapshot.reserve",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_snapshot_used",
            api_path="statistics.snapshot.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_space_available",
            api_path="statistics.space.available",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_space_logical_used",
            api_path="statistics.space.logical_used",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_space_provisioned",
            api_path="statistics.space.provisioned",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_space_reserved_unused",
            api_path="statistics.space.reserved_unused",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_space_savings",
            api_path="statistics.space.savings",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_space_used",
            api_path="statistics.space.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_space_used_excluding_reserves",
            api_path="statistics.space.used_excluding_reserves",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_space_used_percent",
            api_path="statistics.space.used_percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_statistics_incomplete",
            api_path="statistics.statistics_incomplete",
            default=False,
        ),
        FieldMapping(
            cache_attr="template_name",
            api_path="template.name",
        ),
        FieldMapping(
            cache_attr="template_protocol",
            api_path="template.protocol",
        ),
        FieldMapping(
            cache_attr="template_version",
            api_path="template.version",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san_dataset_element_count",
            api_path="mongo_db_on_san.dataset.element_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san_dataset_replication_factor",
            api_path="mongo_db_on_san.dataset.replication_factor",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san_dataset_size",
            api_path="mongo_db_on_san.dataset.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san_dataset_storage_service_name",
            api_path="mongo_db_on_san.dataset.storage_service.name",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san_new_igroups",
            transform=_transform_mongo_db_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san_os_type",
            api_path="mongo_db_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san_primary_igroup_name",
            api_path="mongo_db_on_san.primary_igroup_name",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san_protection_type_local_rpo",
            api_path="mongo_db_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san_protection_type_remote_rpo",
            api_path="mongo_db_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="mongo_db_on_san_secondary_igroups",
            transform=_transform_mongo_db_on_san_secondary_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas_application_components",
            transform=_transform_nas_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas_cifs_access",
            transform=_transform_nas_cifs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas_cifs_share_name",
            api_path="nas.cifs_share_name",
        ),
        FieldMapping(
            cache_attr="nas_exclude_aggregates",
            transform=_transform_nas_exclude_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas_nfs_access",
            transform=_transform_nas_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas_protection_type_local_policy",
            api_path="nas.protection_type.local_policy",
        ),
        FieldMapping(
            cache_attr="nas_protection_type_local_rpo",
            api_path="nas.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="nas_protection_type_remote_rpo",
            api_path="nas.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="nvme_components",
            transform=_transform_nvme_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="nvme_os_type",
            api_path="nvme.os_type",
        ),
        FieldMapping(
            cache_attr="nvme_rpo_local_name",
            api_path="nvme.rpo.local.name",
        ),
        FieldMapping(
            cache_attr="nvme_rpo_local_policy",
            api_path="nvme.rpo.local.policy",
        ),
        FieldMapping(
            cache_attr="nvme_rpo_remote_name",
            api_path="nvme.rpo.remote.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_archive_log_size",
            api_path="oracle_on_nfs.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_archive_log_storage_service_name",
            api_path="oracle_on_nfs.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_db_size",
            api_path="oracle_on_nfs.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_db_storage_service_name",
            api_path="oracle_on_nfs.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_nfs_access",
            transform=_transform_oracle_on_nfs_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_ora_home_size",
            api_path="oracle_on_nfs.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_ora_home_storage_service_name",
            api_path="oracle_on_nfs.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_protection_type_local_rpo",
            api_path="oracle_on_nfs.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_protection_type_remote_rpo",
            api_path="oracle_on_nfs.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_redo_log_mirrored",
            api_path="oracle_on_nfs.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_redo_log_size",
            api_path="oracle_on_nfs.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_nfs_redo_log_storage_service_name",
            api_path="oracle_on_nfs.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san_archive_log_size",
            api_path="oracle_on_san.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san_archive_log_storage_service_name",
            api_path="oracle_on_san.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san_db_size",
            api_path="oracle_on_san.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san_db_storage_service_name",
            api_path="oracle_on_san.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san_igroup_name",
            api_path="oracle_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san_new_igroups",
            transform=_transform_oracle_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_on_san_ora_home_size",
            api_path="oracle_on_san.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san_ora_home_storage_service_name",
            api_path="oracle_on_san.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_on_san_os_type",
            api_path="oracle_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="oracle_on_san_protection_type_local_rpo",
            api_path="oracle_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_san_protection_type_remote_rpo",
            api_path="oracle_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_on_san_redo_log_mirrored",
            api_path="oracle_on_san.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_on_san_redo_log_size",
            api_path="oracle_on_san.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_on_san_redo_log_storage_service_name",
            api_path="oracle_on_san.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_archive_log_size",
            api_path="oracle_rac_on_nfs.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_archive_log_storage_service_name",
            api_path="oracle_rac_on_nfs.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_db_size",
            api_path="oracle_rac_on_nfs.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_db_storage_service_name",
            api_path="oracle_rac_on_nfs.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_grid_binary_size",
            api_path="oracle_rac_on_nfs.grid_binary.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_grid_binary_storage_service_name",
            api_path="oracle_rac_on_nfs.grid_binary.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_nfs_access",
            transform=_transform_oracle_rac_on_nfs_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_ora_home_size",
            api_path="oracle_rac_on_nfs.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_ora_home_storage_service_name",
            api_path="oracle_rac_on_nfs.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_oracle_crs_copies",
            api_path="oracle_rac_on_nfs.oracle_crs.copies",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_oracle_crs_size",
            api_path="oracle_rac_on_nfs.oracle_crs.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_oracle_crs_storage_service_name",
            api_path="oracle_rac_on_nfs.oracle_crs.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_protection_type_local_rpo",
            api_path="oracle_rac_on_nfs.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_protection_type_remote_rpo",
            api_path="oracle_rac_on_nfs.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_redo_log_mirrored",
            api_path="oracle_rac_on_nfs.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_redo_log_size",
            api_path="oracle_rac_on_nfs.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_nfs_redo_log_storage_service_name",
            api_path="oracle_rac_on_nfs.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_archive_log_size",
            api_path="oracle_rac_on_san.archive_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_archive_log_storage_service_name",
            api_path="oracle_rac_on_san.archive_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_db_size",
            api_path="oracle_rac_on_san.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_db_storage_service_name",
            api_path="oracle_rac_on_san.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_db_sids",
            transform=_transform_oracle_rac_on_san_db_sids,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_grid_binary_size",
            api_path="oracle_rac_on_san.grid_binary.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_grid_binary_storage_service_name",
            api_path="oracle_rac_on_san.grid_binary.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_new_igroups",
            transform=_transform_oracle_rac_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_ora_home_size",
            api_path="oracle_rac_on_san.ora_home.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_ora_home_storage_service_name",
            api_path="oracle_rac_on_san.ora_home.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_oracle_crs_copies",
            api_path="oracle_rac_on_san.oracle_crs.copies",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_oracle_crs_size",
            api_path="oracle_rac_on_san.oracle_crs.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_oracle_crs_storage_service_name",
            api_path="oracle_rac_on_san.oracle_crs.storage_service.name",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_os_type",
            api_path="oracle_rac_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_protection_type_local_rpo",
            api_path="oracle_rac_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_protection_type_remote_rpo",
            api_path="oracle_rac_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_redo_log_mirrored",
            api_path="oracle_rac_on_san.redo_log.mirrored",
            default=False,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_redo_log_size",
            api_path="oracle_rac_on_san.redo_log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="oracle_rac_on_san_redo_log_storage_service_name",
            api_path="oracle_rac_on_san.redo_log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="s3_bucket_application_components",
            transform=_transform_s3_bucket_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="s3_bucket_protection_type_remote_rpo",
            api_path="s3_bucket.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="san_application_components",
            transform=_transform_san_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="san_exclude_aggregates",
            transform=_transform_san_exclude_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="san_new_igroups",
            transform=_transform_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="san_os_type",
            api_path="san.os_type",
        ),
        FieldMapping(
            cache_attr="san_protection_type_local_policy",
            api_path="san.protection_type.local_policy",
        ),
        FieldMapping(
            cache_attr="san_protection_type_local_rpo",
            api_path="san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="san_protection_type_remote_rpo",
            api_path="san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_san_db_size",
            api_path="sql_on_san.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san_db_storage_service_name",
            api_path="sql_on_san.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_san_igroup_name",
            api_path="sql_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="sql_on_san_log_size",
            api_path="sql_on_san.log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san_log_storage_service_name",
            api_path="sql_on_san.log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_san_new_igroups",
            transform=_transform_sql_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="sql_on_san_os_type",
            api_path="sql_on_san.os_type",
        ),
        FieldMapping(
            cache_attr="sql_on_san_protection_type_local_rpo",
            api_path="sql_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_san_protection_type_remote_rpo",
            api_path="sql_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_san_server_cores_count",
            api_path="sql_on_san.server_cores_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san_temp_db_size",
            api_path="sql_on_san.temp_db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_san_temp_db_storage_service_name",
            api_path="sql_on_san.temp_db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_smb_access_installer",
            api_path="sql_on_smb.access.installer",
        ),
        FieldMapping(
            cache_attr="sql_on_smb_access_service_account",
            api_path="sql_on_smb.access.service_account",
        ),
        FieldMapping(
            cache_attr="sql_on_smb_db_size",
            api_path="sql_on_smb.db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb_db_storage_service_name",
            api_path="sql_on_smb.db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_smb_log_size",
            api_path="sql_on_smb.log.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb_log_storage_service_name",
            api_path="sql_on_smb.log.storage_service.name",
        ),
        FieldMapping(
            cache_attr="sql_on_smb_protection_type_local_rpo",
            api_path="sql_on_smb.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_smb_protection_type_remote_rpo",
            api_path="sql_on_smb.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="sql_on_smb_server_cores_count",
            api_path="sql_on_smb.server_cores_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb_temp_db_size",
            api_path="sql_on_smb.temp_db.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="sql_on_smb_temp_db_storage_service_name",
            api_path="sql_on_smb.temp_db.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas_desktops_count",
            api_path="vdi_on_nas.desktops.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_nas_desktops_size",
            api_path="vdi_on_nas.desktops.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_nas_desktops_storage_service_name",
            api_path="vdi_on_nas.desktops.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas_hyper_v_access_service_account",
            api_path="vdi_on_nas.hyper_v_access.service_account",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas_nfs_access",
            transform=_transform_vdi_on_nas_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="vdi_on_nas_protection_type_local_rpo",
            api_path="vdi_on_nas.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vdi_on_nas_protection_type_remote_rpo",
            api_path="vdi_on_nas.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="vdi_on_san_desktops_count",
            api_path="vdi_on_san.desktops.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_san_desktops_size",
            api_path="vdi_on_san.desktops.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vdi_on_san_desktops_storage_service_name",
            api_path="vdi_on_san.desktops.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vdi_on_san_hypervisor",
            api_path="vdi_on_san.hypervisor",
        ),
        FieldMapping(
            cache_attr="vdi_on_san_igroup_name",
            api_path="vdi_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="vdi_on_san_new_igroups",
            transform=_transform_vdi_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="vdi_on_san_protection_type_local_rpo",
            api_path="vdi_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vdi_on_san_protection_type_remote_rpo",
            api_path="vdi_on_san.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas_datastore_count",
            api_path="vsi_on_nas.datastore.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_nas_datastore_size",
            api_path="vsi_on_nas.datastore.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_nas_datastore_storage_service_name",
            api_path="vsi_on_nas.datastore.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas_hyper_v_access_service_account",
            api_path="vsi_on_nas.hyper_v_access.service_account",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas_nfs_access",
            transform=_transform_vsi_on_nas_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="vsi_on_nas_protection_type_local_rpo",
            api_path="vsi_on_nas.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_nas_protection_type_remote_rpo",
            api_path="vsi_on_nas.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_san_datastore_count",
            api_path="vsi_on_san.datastore.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_san_datastore_size",
            api_path="vsi_on_san.datastore.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsi_on_san_datastore_storage_service_name",
            api_path="vsi_on_san.datastore.storage_service.name",
        ),
        FieldMapping(
            cache_attr="vsi_on_san_hypervisor",
            api_path="vsi_on_san.hypervisor",
        ),
        FieldMapping(
            cache_attr="vsi_on_san_igroup_name",
            api_path="vsi_on_san.igroup_name",
        ),
        FieldMapping(
            cache_attr="vsi_on_san_new_igroups",
            transform=_transform_vsi_on_san_new_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="vsi_on_san_protection_type_local_rpo",
            api_path="vsi_on_san.protection_type.local_rpo",
        ),
        FieldMapping(
            cache_attr="vsi_on_san_protection_type_remote_rpo",
            api_path="vsi_on_san.protection_type.remote_rpo",
        ),
    ),
)

model_registry.register_mapping("OntapApplication", ONTAPAPPLICATION_MAPPING)
