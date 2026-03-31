"""OntapApplicationTemplate information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapApplicationTemplateNewIgroup(OntapModel):
    """OntapApplicationTemplateNewIgroup sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[dict[str, Any]] = Field(default_factory=list)
    initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationTemplateSecondaryIgroup(OntapModel):
    """OntapApplicationTemplateSecondaryIgroup sub-model for secondary_igroups."""

    name: str = ""


class OntapApplicationTemplateApplicationComponent(OntapModel):
    """OntapApplicationTemplateApplicationComponent sub-model for application_components."""

    name: str = ""
    export_policy_name: str = ""
    export_policy_id: int = 0
    flexcache_dr_cache: bool = False
    flexcache_origin_svm_name: str = ""
    flexcache_origin_component_name: str = ""
    qos_policy_uuid: str = ""
    qos_policy_name: str = ""
    scale_out: bool = False
    share_count: int = 0
    snaplock_append_mode_enabled: bool = False
    snaplock_autocommit_period: str = ""
    snaplock_retention_default: str = ""
    snaplock_retention_minimum: str = ""
    snaplock_retention_maximum: str = ""
    snaplock_snaplock_type: str = ""
    snapshot_locking_enabled: bool = False
    storage_service_name: str = ""
    tiering_control: str = ""
    tiering_object_stores: list[dict[str, Any]] = Field(default_factory=list)
    tiering_policy: str = ""
    total_size: int = 0


class OntapApplicationTemplateCifsAccess(OntapModel):
    """OntapApplicationTemplateCifsAccess sub-model for cifs_access."""

    access: str = ""
    user_or_group: str = ""


class OntapApplicationTemplateExcludeAggregate(OntapModel):
    """OntapApplicationTemplateExcludeAggregate sub-model for exclude_aggregates."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateNfsAccess(OntapModel):
    """OntapApplicationTemplateNfsAccess sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationTemplateComponent(OntapModel):
    """OntapApplicationTemplateComponent sub-model for components."""

    name: str = ""
    namespace_count: int = 0
    os_type: str = ""
    performance_storage_service_name: str = ""
    qos_policy_uuid: str = ""
    qos_policy_name: str = ""
    subsystem_uuid: str = ""
    subsystem_name: str = ""
    subsystem_hosts: list[dict[str, Any]] = Field(default_factory=list)
    subsystem_os_type: str = ""
    tiering_control: str = ""
    tiering_object_stores: list[dict[str, Any]] = Field(default_factory=list)
    tiering_policy: str = ""
    total_size: int = 0


class OntapApplicationTemplateNfsAccess2(OntapModel):
    """OntapApplicationTemplateNfsAccess2 sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationTemplateNewIgroup2(OntapModel):
    """OntapApplicationTemplateNewIgroup2 sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[dict[str, Any]] = Field(default_factory=list)
    initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationTemplateNfsAccess3(OntapModel):
    """OntapApplicationTemplateNfsAccess3 sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationTemplateDbSid(OntapModel):
    """OntapApplicationTemplateDbSid sub-model for db_sids."""

    igroup_name: str = ""


class OntapApplicationTemplateNewIgroup3(OntapModel):
    """OntapApplicationTemplateNewIgroup3 sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[dict[str, Any]] = Field(default_factory=list)
    initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationTemplateApplicationComponent2(OntapModel):
    """OntapApplicationTemplateApplicationComponent2 sub-model for application_components."""

    uuid: str = ""
    name: str = ""
    access_policies: list[dict[str, Any]] = Field(default_factory=list)
    bucket_endpoint_type: str = ""
    capacity_tier: bool = False
    comment: str = ""
    default_retention_period: str = ""
    exclude_aggregates: list[dict[str, Any]] = Field(default_factory=list)
    nas_path: str = ""
    qos_policy_uuid: str = ""
    qos_policy_name: str = ""
    retention_mode: str = ""
    size: int = 0
    storage_service_name: str = ""
    versioning_state: str = ""


class OntapApplicationTemplateApplicationComponent3(OntapModel):
    """OntapApplicationTemplateApplicationComponent3 sub-model for application_components."""

    name: str = ""
    igroup_name: str = ""
    lun_count: int = 0
    os_type: str = ""
    qos_policy_uuid: str = ""
    qos_policy_name: str = ""
    storage_service_name: str = ""
    tiering_control: str = ""
    tiering_object_stores: list[dict[str, Any]] = Field(default_factory=list)
    tiering_policy: str = ""
    total_size: int = 0


class OntapApplicationTemplateExcludeAggregate2(OntapModel):
    """OntapApplicationTemplateExcludeAggregate2 sub-model for exclude_aggregates."""

    uuid: str = ""
    name: str = ""


class OntapApplicationTemplateNewIgroup4(OntapModel):
    """OntapApplicationTemplateNewIgroup4 sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[dict[str, Any]] = Field(default_factory=list)
    initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationTemplateNewIgroup5(OntapModel):
    """OntapApplicationTemplateNewIgroup5 sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[dict[str, Any]] = Field(default_factory=list)
    initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    initiators: list[str] = Field(default_factory=list)
    os_type: str = ""
    protocol: str = ""


class OntapApplicationTemplateNfsAccess4(OntapModel):
    """OntapApplicationTemplateNfsAccess4 sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationTemplateNewIgroup6(OntapModel):
    """OntapApplicationTemplateNewIgroup6 sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[dict[str, Any]] = Field(default_factory=list)
    initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    initiators: list[str] = Field(default_factory=list)
    protocol: str = ""


class OntapApplicationTemplateNfsAccess5(OntapModel):
    """OntapApplicationTemplateNfsAccess5 sub-model for nfs_access."""

    access: str = ""
    host: str = ""


class OntapApplicationTemplateNewIgroup7(OntapModel):
    """OntapApplicationTemplateNewIgroup7 sub-model for new_igroups."""

    name: str = ""
    comment: str = ""
    igroups: list[dict[str, Any]] = Field(default_factory=list)
    initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    initiators: list[str] = Field(default_factory=list)
    protocol: str = ""


class OntapApplicationTemplate(OntapModel):
    """OntapApplicationTemplate information."""

    name: str = ""
    description: str = ""
    missing_prerequisites: str = ""
    mongo_db_on_san_dataset_element_count: int = 0
    mongo_db_on_san_dataset_replication_factor: int = 0
    mongo_db_on_san_dataset_size: int = 0
    mongo_db_on_san_dataset_storage_service_name: str = ""
    mongo_db_on_san_new_igroups: list[OntapApplicationTemplateNewIgroup] = Field(
        default_factory=list
    )
    mongo_db_on_san_os_type: str = ""
    mongo_db_on_san_primary_igroup_name: str = ""
    mongo_db_on_san_protection_type_local_rpo: str = ""
    mongo_db_on_san_protection_type_remote_rpo: str = ""
    mongo_db_on_san_secondary_igroups: list[OntapApplicationTemplateSecondaryIgroup] = Field(
        default_factory=list
    )
    nas_application_components: list[OntapApplicationTemplateApplicationComponent] = Field(
        default_factory=list
    )
    nas_cifs_access: list[OntapApplicationTemplateCifsAccess] = Field(default_factory=list)
    nas_cifs_share_name: str = ""
    nas_exclude_aggregates: list[OntapApplicationTemplateExcludeAggregate] = Field(
        default_factory=list
    )
    nas_nfs_access: list[OntapApplicationTemplateNfsAccess] = Field(default_factory=list)
    nas_protection_type_local_policy: str = ""
    nas_protection_type_local_rpo: str = ""
    nas_protection_type_remote_rpo: str = ""
    nvme_components: list[OntapApplicationTemplateComponent] = Field(default_factory=list)
    nvme_os_type: str = ""
    nvme_rpo_local_name: str = ""
    nvme_rpo_local_policy: str = ""
    nvme_rpo_remote_name: str = ""
    oracle_on_nfs_archive_log_size: int = 0
    oracle_on_nfs_archive_log_storage_service_name: str = ""
    oracle_on_nfs_db_size: int = 0
    oracle_on_nfs_db_storage_service_name: str = ""
    oracle_on_nfs_nfs_access: list[OntapApplicationTemplateNfsAccess2] = Field(default_factory=list)
    oracle_on_nfs_ora_home_size: int = 0
    oracle_on_nfs_ora_home_storage_service_name: str = ""
    oracle_on_nfs_protection_type_local_rpo: str = ""
    oracle_on_nfs_protection_type_remote_rpo: str = ""
    oracle_on_nfs_redo_log_mirrored: bool = False
    oracle_on_nfs_redo_log_size: int = 0
    oracle_on_nfs_redo_log_storage_service_name: str = ""
    oracle_on_san_archive_log_size: int = 0
    oracle_on_san_archive_log_storage_service_name: str = ""
    oracle_on_san_db_size: int = 0
    oracle_on_san_db_storage_service_name: str = ""
    oracle_on_san_igroup_name: str = ""
    oracle_on_san_new_igroups: list[OntapApplicationTemplateNewIgroup2] = Field(
        default_factory=list
    )
    oracle_on_san_ora_home_size: int = 0
    oracle_on_san_ora_home_storage_service_name: str = ""
    oracle_on_san_os_type: str = ""
    oracle_on_san_protection_type_local_rpo: str = ""
    oracle_on_san_protection_type_remote_rpo: str = ""
    oracle_on_san_redo_log_mirrored: bool = False
    oracle_on_san_redo_log_size: int = 0
    oracle_on_san_redo_log_storage_service_name: str = ""
    oracle_rac_on_nfs_archive_log_size: int = 0
    oracle_rac_on_nfs_archive_log_storage_service_name: str = ""
    oracle_rac_on_nfs_db_size: int = 0
    oracle_rac_on_nfs_db_storage_service_name: str = ""
    oracle_rac_on_nfs_grid_binary_size: int = 0
    oracle_rac_on_nfs_grid_binary_storage_service_name: str = ""
    oracle_rac_on_nfs_nfs_access: list[OntapApplicationTemplateNfsAccess3] = Field(
        default_factory=list
    )
    oracle_rac_on_nfs_ora_home_size: int = 0
    oracle_rac_on_nfs_ora_home_storage_service_name: str = ""
    oracle_rac_on_nfs_oracle_crs_copies: int = 0
    oracle_rac_on_nfs_oracle_crs_size: int = 0
    oracle_rac_on_nfs_oracle_crs_storage_service_name: str = ""
    oracle_rac_on_nfs_protection_type_local_rpo: str = ""
    oracle_rac_on_nfs_protection_type_remote_rpo: str = ""
    oracle_rac_on_nfs_redo_log_mirrored: bool = False
    oracle_rac_on_nfs_redo_log_size: int = 0
    oracle_rac_on_nfs_redo_log_storage_service_name: str = ""
    oracle_rac_on_san_archive_log_size: int = 0
    oracle_rac_on_san_archive_log_storage_service_name: str = ""
    oracle_rac_on_san_db_size: int = 0
    oracle_rac_on_san_db_storage_service_name: str = ""
    oracle_rac_on_san_db_sids: list[OntapApplicationTemplateDbSid] = Field(default_factory=list)
    oracle_rac_on_san_grid_binary_size: int = 0
    oracle_rac_on_san_grid_binary_storage_service_name: str = ""
    oracle_rac_on_san_new_igroups: list[OntapApplicationTemplateNewIgroup3] = Field(
        default_factory=list
    )
    oracle_rac_on_san_ora_home_size: int = 0
    oracle_rac_on_san_ora_home_storage_service_name: str = ""
    oracle_rac_on_san_oracle_crs_copies: int = 0
    oracle_rac_on_san_oracle_crs_size: int = 0
    oracle_rac_on_san_oracle_crs_storage_service_name: str = ""
    oracle_rac_on_san_os_type: str = ""
    oracle_rac_on_san_protection_type_local_rpo: str = ""
    oracle_rac_on_san_protection_type_remote_rpo: str = ""
    oracle_rac_on_san_redo_log_mirrored: bool = False
    oracle_rac_on_san_redo_log_size: int = 0
    oracle_rac_on_san_redo_log_storage_service_name: str = ""
    protocol: str = ""
    s3_bucket_application_components: list[OntapApplicationTemplateApplicationComponent2] = Field(
        default_factory=list
    )
    s3_bucket_protection_type_remote_rpo: str = ""
    san_application_components: list[OntapApplicationTemplateApplicationComponent3] = Field(
        default_factory=list
    )
    san_exclude_aggregates: list[OntapApplicationTemplateExcludeAggregate2] = Field(
        default_factory=list
    )
    san_new_igroups: list[OntapApplicationTemplateNewIgroup4] = Field(default_factory=list)
    san_os_type: str = ""
    san_protection_type_local_policy: str = ""
    san_protection_type_local_rpo: str = ""
    san_protection_type_remote_rpo: str = ""
    sql_on_san_db_size: int = 0
    sql_on_san_db_storage_service_name: str = ""
    sql_on_san_igroup_name: str = ""
    sql_on_san_log_size: int = 0
    sql_on_san_log_storage_service_name: str = ""
    sql_on_san_new_igroups: list[OntapApplicationTemplateNewIgroup5] = Field(default_factory=list)
    sql_on_san_os_type: str = ""
    sql_on_san_protection_type_local_rpo: str = ""
    sql_on_san_protection_type_remote_rpo: str = ""
    sql_on_san_server_cores_count: int = 0
    sql_on_san_temp_db_size: int = 0
    sql_on_san_temp_db_storage_service_name: str = ""
    sql_on_smb_access_installer: str = ""
    sql_on_smb_access_service_account: str = ""
    sql_on_smb_db_size: int = 0
    sql_on_smb_db_storage_service_name: str = ""
    sql_on_smb_log_size: int = 0
    sql_on_smb_log_storage_service_name: str = ""
    sql_on_smb_protection_type_local_rpo: str = ""
    sql_on_smb_protection_type_remote_rpo: str = ""
    sql_on_smb_server_cores_count: int = 0
    sql_on_smb_temp_db_size: int = 0
    sql_on_smb_temp_db_storage_service_name: str = ""
    vdi_on_nas_desktops_count: int = 0
    vdi_on_nas_desktops_size: int = 0
    vdi_on_nas_desktops_storage_service_name: str = ""
    vdi_on_nas_hyper_v_access_service_account: str = ""
    vdi_on_nas_nfs_access: list[OntapApplicationTemplateNfsAccess4] = Field(default_factory=list)
    vdi_on_nas_protection_type_local_rpo: str = ""
    vdi_on_nas_protection_type_remote_rpo: str = ""
    vdi_on_san_desktops_count: int = 0
    vdi_on_san_desktops_size: int = 0
    vdi_on_san_desktops_storage_service_name: str = ""
    vdi_on_san_hypervisor: str = ""
    vdi_on_san_igroup_name: str = ""
    vdi_on_san_new_igroups: list[OntapApplicationTemplateNewIgroup6] = Field(default_factory=list)
    vdi_on_san_protection_type_local_rpo: str = ""
    vdi_on_san_protection_type_remote_rpo: str = ""
    vsi_on_nas_datastore_count: int = 0
    vsi_on_nas_datastore_size: int = 0
    vsi_on_nas_datastore_storage_service_name: str = ""
    vsi_on_nas_hyper_v_access_service_account: str = ""
    vsi_on_nas_nfs_access: list[OntapApplicationTemplateNfsAccess5] = Field(default_factory=list)
    vsi_on_nas_protection_type_local_rpo: str = ""
    vsi_on_nas_protection_type_remote_rpo: str = ""
    vsi_on_san_datastore_count: int = 0
    vsi_on_san_datastore_size: int = 0
    vsi_on_san_datastore_storage_service_name: str = ""
    vsi_on_san_hypervisor: str = ""
    vsi_on_san_igroup_name: str = ""
    vsi_on_san_new_igroups: list[OntapApplicationTemplateNewIgroup7] = Field(default_factory=list)
    vsi_on_san_protection_type_local_rpo: str = ""
    vsi_on_san_protection_type_remote_rpo: str = ""
