# ruff: noqa: E501
"""OntapApplicationTemplate type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.application.templates.model import (
    OntapApplicationTemplate,
    OntapApplicationTemplateApplicationComponent,
    OntapApplicationTemplateApplicationComponent2,
    OntapApplicationTemplateApplicationComponent3,
    OntapApplicationTemplateCifsAccess,
    OntapApplicationTemplateComponent,
    OntapApplicationTemplateDbSid,
    OntapApplicationTemplateExcludeAggregate,
    OntapApplicationTemplateExcludeAggregate2,
    OntapApplicationTemplateNewIgroup,
    OntapApplicationTemplateNewIgroup2,
    OntapApplicationTemplateNewIgroup3,
    OntapApplicationTemplateNewIgroup4,
    OntapApplicationTemplateNewIgroup5,
    OntapApplicationTemplateNewIgroup6,
    OntapApplicationTemplateNewIgroup7,
    OntapApplicationTemplateNfsAccess,
    OntapApplicationTemplateNfsAccess2,
    OntapApplicationTemplateNfsAccess3,
    OntapApplicationTemplateNfsAccess4,
    OntapApplicationTemplateNfsAccess5,
    OntapApplicationTemplateSecondaryIgroup,
)


def _transform_mongo_db_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNewIgroup]:
    """Transform mongo_db_on_san.new_igroups into OntapApplicationTemplateNewIgroup list."""
    return [
        OntapApplicationTemplateNewIgroup(**item)
        for item in record.get("mongo_db_on_san.new_igroups", [])
    ]


def _transform_mongo_db_on_san_secondary_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateSecondaryIgroup]:
    """Transform mongo_db_on_san.secondary_igroups into OntapApplicationTemplateSecondaryIgroup list."""
    return [
        OntapApplicationTemplateSecondaryIgroup(**item)
        for item in record.get("mongo_db_on_san.secondary_igroups", [])
    ]


def _transform_nas_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateApplicationComponent]:
    """Transform nas.application_components into OntapApplicationTemplateApplicationComponent list."""
    return [
        OntapApplicationTemplateApplicationComponent(**item)
        for item in record.get("nas.application_components", [])
    ]


def _transform_nas_cifs_access(record: dict[str, Any]) -> list[OntapApplicationTemplateCifsAccess]:
    """Transform nas.cifs_access into OntapApplicationTemplateCifsAccess list."""
    return [
        OntapApplicationTemplateCifsAccess(**item) for item in record.get("nas.cifs_access", [])
    ]


def _transform_nas_exclude_aggregates(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateExcludeAggregate]:
    """Transform nas.exclude_aggregates into OntapApplicationTemplateExcludeAggregate list."""
    return [
        OntapApplicationTemplateExcludeAggregate(**item)
        for item in record.get("nas.exclude_aggregates", [])
    ]


def _transform_nas_nfs_access(record: dict[str, Any]) -> list[OntapApplicationTemplateNfsAccess]:
    """Transform nas.nfs_access into OntapApplicationTemplateNfsAccess list."""
    return [OntapApplicationTemplateNfsAccess(**item) for item in record.get("nas.nfs_access", [])]


def _transform_nvme_components(record: dict[str, Any]) -> list[OntapApplicationTemplateComponent]:
    """Transform nvme.components into OntapApplicationTemplateComponent list."""
    return [OntapApplicationTemplateComponent(**item) for item in record.get("nvme.components", [])]


def _transform_oracle_on_nfs_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNfsAccess2]:
    """Transform oracle_on_nfs.nfs_access into OntapApplicationTemplateNfsAccess2 list."""
    return [
        OntapApplicationTemplateNfsAccess2(**item)
        for item in record.get("oracle_on_nfs.nfs_access", [])
    ]


def _transform_oracle_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNewIgroup2]:
    """Transform oracle_on_san.new_igroups into OntapApplicationTemplateNewIgroup2 list."""
    return [
        OntapApplicationTemplateNewIgroup2(**item)
        for item in record.get("oracle_on_san.new_igroups", [])
    ]


def _transform_oracle_rac_on_nfs_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNfsAccess3]:
    """Transform oracle_rac_on_nfs.nfs_access into OntapApplicationTemplateNfsAccess3 list."""
    return [
        OntapApplicationTemplateNfsAccess3(**item)
        for item in record.get("oracle_rac_on_nfs.nfs_access", [])
    ]


def _transform_oracle_rac_on_san_db_sids(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateDbSid]:
    """Transform oracle_rac_on_san.db_sids into OntapApplicationTemplateDbSid list."""
    return [
        OntapApplicationTemplateDbSid(**item)
        for item in record.get("oracle_rac_on_san.db_sids", [])
    ]


def _transform_oracle_rac_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNewIgroup3]:
    """Transform oracle_rac_on_san.new_igroups into OntapApplicationTemplateNewIgroup3 list."""
    return [
        OntapApplicationTemplateNewIgroup3(**item)
        for item in record.get("oracle_rac_on_san.new_igroups", [])
    ]


def _transform_s3_bucket_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateApplicationComponent2]:
    """Transform s3_bucket.application_components into OntapApplicationTemplateApplicationComponent2 list."""
    return [
        OntapApplicationTemplateApplicationComponent2(**item)
        for item in record.get("s3_bucket.application_components", [])
    ]


def _transform_san_application_components(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateApplicationComponent3]:
    """Transform san.application_components into OntapApplicationTemplateApplicationComponent3 list."""
    return [
        OntapApplicationTemplateApplicationComponent3(**item)
        for item in record.get("san.application_components", [])
    ]


def _transform_san_exclude_aggregates(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateExcludeAggregate2]:
    """Transform san.exclude_aggregates into OntapApplicationTemplateExcludeAggregate2 list."""
    return [
        OntapApplicationTemplateExcludeAggregate2(**item)
        for item in record.get("san.exclude_aggregates", [])
    ]


def _transform_san_new_igroups(record: dict[str, Any]) -> list[OntapApplicationTemplateNewIgroup4]:
    """Transform san.new_igroups into OntapApplicationTemplateNewIgroup4 list."""
    return [
        OntapApplicationTemplateNewIgroup4(**item) for item in record.get("san.new_igroups", [])
    ]


def _transform_sql_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNewIgroup5]:
    """Transform sql_on_san.new_igroups into OntapApplicationTemplateNewIgroup5 list."""
    return [
        OntapApplicationTemplateNewIgroup5(**item)
        for item in record.get("sql_on_san.new_igroups", [])
    ]


def _transform_vdi_on_nas_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNfsAccess4]:
    """Transform vdi_on_nas.nfs_access into OntapApplicationTemplateNfsAccess4 list."""
    return [
        OntapApplicationTemplateNfsAccess4(**item)
        for item in record.get("vdi_on_nas.nfs_access", [])
    ]


def _transform_vdi_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNewIgroup6]:
    """Transform vdi_on_san.new_igroups into OntapApplicationTemplateNewIgroup6 list."""
    return [
        OntapApplicationTemplateNewIgroup6(**item)
        for item in record.get("vdi_on_san.new_igroups", [])
    ]


def _transform_vsi_on_nas_nfs_access(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNfsAccess5]:
    """Transform vsi_on_nas.nfs_access into OntapApplicationTemplateNfsAccess5 list."""
    return [
        OntapApplicationTemplateNfsAccess5(**item)
        for item in record.get("vsi_on_nas.nfs_access", [])
    ]


def _transform_vsi_on_san_new_igroups(
    record: dict[str, Any],
) -> list[OntapApplicationTemplateNewIgroup7]:
    """Transform vsi_on_san.new_igroups into OntapApplicationTemplateNewIgroup7 list."""
    return [
        OntapApplicationTemplateNewIgroup7(**item)
        for item in record.get("vsi_on_san.new_igroups", [])
    ]


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
            api_path="mongo_db_on_san.new_igroups",
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
            api_path="mongo_db_on_san.secondary_igroups",
            transform=_transform_mongo_db_on_san_secondary_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas_application_components",
            api_path="nas.application_components",
            transform=_transform_nas_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas_cifs_access",
            api_path="nas.cifs_access",
            transform=_transform_nas_cifs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas_cifs_share_name",
            api_path="nas.cifs_share_name",
        ),
        FieldMapping(
            cache_attr="nas_exclude_aggregates",
            api_path="nas.exclude_aggregates",
            transform=_transform_nas_exclude_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="nas_nfs_access",
            api_path="nas.nfs_access",
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
            api_path="nvme.components",
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
            api_path="oracle_on_nfs.nfs_access",
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
            api_path="oracle_on_san.new_igroups",
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
            api_path="oracle_rac_on_nfs.nfs_access",
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
            api_path="oracle_rac_on_san.db_sids",
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
            api_path="oracle_rac_on_san.new_igroups",
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
            cache_attr="protocol",
            api_path="protocol",
        ),
        FieldMapping(
            cache_attr="s3_bucket_application_components",
            api_path="s3_bucket.application_components",
            transform=_transform_s3_bucket_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="s3_bucket_protection_type_remote_rpo",
            api_path="s3_bucket.protection_type.remote_rpo",
        ),
        FieldMapping(
            cache_attr="san_application_components",
            api_path="san.application_components",
            transform=_transform_san_application_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="san_exclude_aggregates",
            api_path="san.exclude_aggregates",
            transform=_transform_san_exclude_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="san_new_igroups",
            api_path="san.new_igroups",
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
            api_path="sql_on_san.new_igroups",
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
            api_path="vdi_on_nas.nfs_access",
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
            api_path="vdi_on_san.new_igroups",
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
            api_path="vsi_on_nas.nfs_access",
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
            api_path="vsi_on_san.new_igroups",
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

model_registry.register_mapping("OntapApplicationTemplate", ONTAPAPPLICATIONTEMPLATE_MAPPING)
