"""OntapApplication information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapApplicationComponent(CacheModel):
    """OntapApplicationComponent sub-model for components."""

    rpo_components_uuid: str = ""
    rpo_components_name: str = ""
    rpo_components_rpo_local_name: str = ""
    rpo_components_rpo_local_description: str = ""
    rpo_components_rpo_remote_name: str = ""
    rpo_components_rpo_remote_description: str = ""


class OntapApplicationComponent2(CacheModel):
    """OntapApplicationComponent2 sub-model for components."""

    statistics_components_uuid: str = ""
    statistics_components_name: str = ""
    statistics_components_iops_per_tb: int = 0
    statistics_components_iops_total: int = 0
    statistics_components_latency_average: int = 0
    statistics_components_latency_raw: int = 0
    statistics_components_shared_storage_pool: bool = False
    statistics_components_snapshot_reserve: int = 0
    statistics_components_snapshot_used: int = 0
    statistics_components_space_available: int = 0
    statistics_components_space_logical_used: int = 0
    statistics_components_space_provisioned: int = 0
    statistics_components_space_reserved_unused: int = 0
    statistics_components_space_savings: int = 0
    statistics_components_space_used: int = 0
    statistics_components_space_used_excluding_reserves: int = 0
    statistics_components_space_used_percent: int = 0
    statistics_components_statistics_incomplete: bool = False
    statistics_components_storage_service_uuid: str = ""
    statistics_components_storage_service_name: str = ""


class OntapApplicationNewIgroup(CacheModel):
    """OntapApplicationNewIgroup sub-model for new_igroups."""

    mongo_db_on_san_new_igroups_name: str = ""
    mongo_db_on_san_new_igroups_comment: str = ""
    mongo_db_on_san_new_igroups_igroups: list[dict[str, Any]] = Field(default_factory=list)
    mongo_db_on_san_new_igroups_initiator_objects: list[dict[str, Any]] = Field(
        default_factory=list
    )
    mongo_db_on_san_new_igroups_initiators: list[str] = Field(default_factory=list)
    mongo_db_on_san_new_igroups_os_type: str = ""
    mongo_db_on_san_new_igroups_protocol: str = ""


class OntapApplicationSecondaryIgroup(CacheModel):
    """OntapApplicationSecondaryIgroup sub-model for secondary_igroups."""

    mongo_db_on_san_secondary_igroups_name: str = ""


class OntapApplicationApplicationComponent(CacheModel):
    """OntapApplicationApplicationComponent sub-model for application_components."""

    nas_application_components_name: str = ""
    nas_application_components_export_policy_name: str = ""
    nas_application_components_export_policy_id: int = 0
    nas_application_components_flexcache_dr_cache: bool = False
    nas_application_components_flexcache_origin_svm_name: str = ""
    nas_application_components_flexcache_origin_component_name: str = ""
    nas_application_components_qos_policy_uuid: str = ""
    nas_application_components_qos_policy_name: str = ""
    nas_application_components_scale_out: bool = False
    nas_application_components_share_count: int = 0
    nas_application_components_snaplock_append_mode_enabled: bool = False
    nas_application_components_snaplock_autocommit_period: str = ""
    nas_application_components_snaplock_retention_default: str = ""
    nas_application_components_snaplock_retention_minimum: str = ""
    nas_application_components_snaplock_retention_maximum: str = ""
    nas_application_components_snaplock_snaplock_type: str = ""
    nas_application_components_snapshot_locking_enabled: bool = False
    nas_application_components_storage_service_name: str = ""
    nas_application_components_tiering_control: str = ""
    nas_application_components_tiering_object_stores: list[dict[str, Any]] = Field(
        default_factory=list
    )
    nas_application_components_tiering_policy: str = ""
    nas_application_components_total_size: int = 0


class OntapApplicationCifsAccess(CacheModel):
    """OntapApplicationCifsAccess sub-model for cifs_access."""

    nas_cifs_access_access: str = ""
    nas_cifs_access_user_or_group: str = ""


class OntapApplicationExcludeAggregate(CacheModel):
    """OntapApplicationExcludeAggregate sub-model for exclude_aggregates."""

    nas_exclude_aggregates_uuid: str = ""
    nas_exclude_aggregates_name: str = ""


class OntapApplicationNfsAccess(CacheModel):
    """OntapApplicationNfsAccess sub-model for nfs_access."""

    nas_nfs_access_access: str = ""
    nas_nfs_access_host: str = ""


class OntapApplicationComponent3(CacheModel):
    """OntapApplicationComponent3 sub-model for components."""

    nvme_components_name: str = ""
    nvme_components_namespace_count: int = 0
    nvme_components_os_type: str = ""
    nvme_components_performance_storage_service_name: str = ""
    nvme_components_qos_policy_uuid: str = ""
    nvme_components_qos_policy_name: str = ""
    nvme_components_subsystem_uuid: str = ""
    nvme_components_subsystem_name: str = ""
    nvme_components_subsystem_hosts: list[dict[str, Any]] = Field(default_factory=list)
    nvme_components_subsystem_os_type: str = ""
    nvme_components_tiering_control: str = ""
    nvme_components_tiering_object_stores: list[dict[str, Any]] = Field(default_factory=list)
    nvme_components_tiering_policy: str = ""
    nvme_components_total_size: int = 0


class OntapApplicationNfsAccess2(CacheModel):
    """OntapApplicationNfsAccess2 sub-model for nfs_access."""

    oracle_on_nfs_nfs_access_access: str = ""
    oracle_on_nfs_nfs_access_host: str = ""


class OntapApplicationNewIgroup2(CacheModel):
    """OntapApplicationNewIgroup2 sub-model for new_igroups."""

    oracle_on_san_new_igroups_name: str = ""
    oracle_on_san_new_igroups_comment: str = ""
    oracle_on_san_new_igroups_igroups: list[dict[str, Any]] = Field(default_factory=list)
    oracle_on_san_new_igroups_initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    oracle_on_san_new_igroups_initiators: list[str] = Field(default_factory=list)
    oracle_on_san_new_igroups_os_type: str = ""
    oracle_on_san_new_igroups_protocol: str = ""


class OntapApplicationNfsAccess3(CacheModel):
    """OntapApplicationNfsAccess3 sub-model for nfs_access."""

    oracle_rac_on_nfs_nfs_access_access: str = ""
    oracle_rac_on_nfs_nfs_access_host: str = ""


class OntapApplicationDbSid(CacheModel):
    """OntapApplicationDbSid sub-model for db_sids."""

    oracle_rac_on_san_db_sids_igroup_name: str = ""


class OntapApplicationNewIgroup3(CacheModel):
    """OntapApplicationNewIgroup3 sub-model for new_igroups."""

    oracle_rac_on_san_new_igroups_name: str = ""
    oracle_rac_on_san_new_igroups_comment: str = ""
    oracle_rac_on_san_new_igroups_igroups: list[dict[str, Any]] = Field(default_factory=list)
    oracle_rac_on_san_new_igroups_initiator_objects: list[dict[str, Any]] = Field(
        default_factory=list
    )
    oracle_rac_on_san_new_igroups_initiators: list[str] = Field(default_factory=list)
    oracle_rac_on_san_new_igroups_os_type: str = ""
    oracle_rac_on_san_new_igroups_protocol: str = ""


class OntapApplicationApplicationComponent2(CacheModel):
    """OntapApplicationApplicationComponent2 sub-model for application_components."""

    s3_bucket_application_components_uuid: str = ""
    s3_bucket_application_components_name: str = ""
    s3_bucket_application_components_access_policies: list[dict[str, Any]] = Field(
        default_factory=list
    )
    s3_bucket_application_components_bucket_endpoint_type: str = ""
    s3_bucket_application_components_capacity_tier: bool = False
    s3_bucket_application_components_comment: str = ""
    s3_bucket_application_components_default_retention_period: str = ""
    s3_bucket_application_components_exclude_aggregates: list[dict[str, Any]] = Field(
        default_factory=list
    )
    s3_bucket_application_components_nas_path: str = ""
    s3_bucket_application_components_qos_policy_uuid: str = ""
    s3_bucket_application_components_qos_policy_name: str = ""
    s3_bucket_application_components_retention_mode: str = ""
    s3_bucket_application_components_size: int = 0
    s3_bucket_application_components_storage_service_name: str = ""
    s3_bucket_application_components_versioning_state: str = ""


class OntapApplicationApplicationComponent3(CacheModel):
    """OntapApplicationApplicationComponent3 sub-model for application_components."""

    san_application_components_name: str = ""
    san_application_components_igroup_name: str = ""
    san_application_components_lun_count: int = 0
    san_application_components_os_type: str = ""
    san_application_components_qos_policy_uuid: str = ""
    san_application_components_qos_policy_name: str = ""
    san_application_components_storage_service_name: str = ""
    san_application_components_tiering_control: str = ""
    san_application_components_tiering_object_stores: list[dict[str, Any]] = Field(
        default_factory=list
    )
    san_application_components_tiering_policy: str = ""
    san_application_components_total_size: int = 0


class OntapApplicationExcludeAggregate2(CacheModel):
    """OntapApplicationExcludeAggregate2 sub-model for exclude_aggregates."""

    san_exclude_aggregates_uuid: str = ""
    san_exclude_aggregates_name: str = ""


class OntapApplicationNewIgroup4(CacheModel):
    """OntapApplicationNewIgroup4 sub-model for new_igroups."""

    san_new_igroups_name: str = ""
    san_new_igroups_comment: str = ""
    san_new_igroups_igroups: list[dict[str, Any]] = Field(default_factory=list)
    san_new_igroups_initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    san_new_igroups_initiators: list[str] = Field(default_factory=list)
    san_new_igroups_os_type: str = ""
    san_new_igroups_protocol: str = ""


class OntapApplicationNewIgroup5(CacheModel):
    """OntapApplicationNewIgroup5 sub-model for new_igroups."""

    sql_on_san_new_igroups_name: str = ""
    sql_on_san_new_igroups_comment: str = ""
    sql_on_san_new_igroups_igroups: list[dict[str, Any]] = Field(default_factory=list)
    sql_on_san_new_igroups_initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    sql_on_san_new_igroups_initiators: list[str] = Field(default_factory=list)
    sql_on_san_new_igroups_os_type: str = ""
    sql_on_san_new_igroups_protocol: str = ""


class OntapApplicationNfsAccess4(CacheModel):
    """OntapApplicationNfsAccess4 sub-model for nfs_access."""

    vdi_on_nas_nfs_access_access: str = ""
    vdi_on_nas_nfs_access_host: str = ""


class OntapApplicationNewIgroup6(CacheModel):
    """OntapApplicationNewIgroup6 sub-model for new_igroups."""

    vdi_on_san_new_igroups_name: str = ""
    vdi_on_san_new_igroups_comment: str = ""
    vdi_on_san_new_igroups_igroups: list[dict[str, Any]] = Field(default_factory=list)
    vdi_on_san_new_igroups_initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    vdi_on_san_new_igroups_initiators: list[str] = Field(default_factory=list)
    vdi_on_san_new_igroups_protocol: str = ""


class OntapApplicationNfsAccess5(CacheModel):
    """OntapApplicationNfsAccess5 sub-model for nfs_access."""

    vsi_on_nas_nfs_access_access: str = ""
    vsi_on_nas_nfs_access_host: str = ""


class OntapApplicationNewIgroup7(CacheModel):
    """OntapApplicationNewIgroup7 sub-model for new_igroups."""

    vsi_on_san_new_igroups_name: str = ""
    vsi_on_san_new_igroups_comment: str = ""
    vsi_on_san_new_igroups_igroups: list[dict[str, Any]] = Field(default_factory=list)
    vsi_on_san_new_igroups_initiator_objects: list[dict[str, Any]] = Field(default_factory=list)
    vsi_on_san_new_igroups_initiators: list[str] = Field(default_factory=list)
    vsi_on_san_new_igroups_protocol: str = ""


class OntapApplication(CacheModel):
    """OntapApplication information."""

    svm_uuid: str = ""
    svm_name: str = ""
    uuid: str = ""
    name: str = ""
    creation_timestamp: str = ""
    delete_data: bool = False
    generation: int = 0
    protection_granularity: str = ""
    rpo_components: list[OntapApplicationComponent] = Field(default_factory=list)
    rpo_is_supported: bool = False
    rpo_local_name: str = ""
    rpo_local_description: str = ""
    rpo_remote_name: str = ""
    rpo_remote_description: str = ""
    smart_container: bool = False
    state: str = ""
    statistics_components: list[OntapApplicationComponent2] = Field(default_factory=list)
    statistics_iops_per_tb: int = 0
    statistics_iops_total: int = 0
    statistics_latency_average: int = 0
    statistics_latency_raw: int = 0
    statistics_shared_storage_pool: bool = False
    statistics_snapshot_reserve: int = 0
    statistics_snapshot_used: int = 0
    statistics_space_available: int = 0
    statistics_space_logical_used: int = 0
    statistics_space_provisioned: int = 0
    statistics_space_reserved_unused: int = 0
    statistics_space_savings: int = 0
    statistics_space_used: int = 0
    statistics_space_used_excluding_reserves: int = 0
    statistics_space_used_percent: int = 0
    statistics_statistics_incomplete: bool = False
    template_name: str = ""
    template_protocol: str = ""
    template_version: int = 0
    mongo_db_on_san_dataset_element_count: int = 0
    mongo_db_on_san_dataset_replication_factor: int = 0
    mongo_db_on_san_dataset_size: int = 0
    mongo_db_on_san_dataset_storage_service_name: str = ""
    mongo_db_on_san_new_igroups: list[OntapApplicationNewIgroup] = Field(default_factory=list)
    mongo_db_on_san_os_type: str = ""
    mongo_db_on_san_primary_igroup_name: str = ""
    mongo_db_on_san_protection_type_local_rpo: str = ""
    mongo_db_on_san_protection_type_remote_rpo: str = ""
    mongo_db_on_san_secondary_igroups: list[OntapApplicationSecondaryIgroup] = Field(
        default_factory=list
    )
    nas_application_components: list[OntapApplicationApplicationComponent] = Field(
        default_factory=list
    )
    nas_cifs_access: list[OntapApplicationCifsAccess] = Field(default_factory=list)
    nas_cifs_share_name: str = ""
    nas_exclude_aggregates: list[OntapApplicationExcludeAggregate] = Field(default_factory=list)
    nas_nfs_access: list[OntapApplicationNfsAccess] = Field(default_factory=list)
    nas_protection_type_local_policy: str = ""
    nas_protection_type_local_rpo: str = ""
    nas_protection_type_remote_rpo: str = ""
    nvme_components: list[OntapApplicationComponent3] = Field(default_factory=list)
    nvme_os_type: str = ""
    nvme_rpo_local_name: str = ""
    nvme_rpo_local_policy: str = ""
    nvme_rpo_remote_name: str = ""
    oracle_on_nfs_archive_log_size: int = 0
    oracle_on_nfs_archive_log_storage_service_name: str = ""
    oracle_on_nfs_db_size: int = 0
    oracle_on_nfs_db_storage_service_name: str = ""
    oracle_on_nfs_nfs_access: list[OntapApplicationNfsAccess2] = Field(default_factory=list)
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
    oracle_on_san_new_igroups: list[OntapApplicationNewIgroup2] = Field(default_factory=list)
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
    oracle_rac_on_nfs_nfs_access: list[OntapApplicationNfsAccess3] = Field(default_factory=list)
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
    oracle_rac_on_san_db_sids: list[OntapApplicationDbSid] = Field(default_factory=list)
    oracle_rac_on_san_grid_binary_size: int = 0
    oracle_rac_on_san_grid_binary_storage_service_name: str = ""
    oracle_rac_on_san_new_igroups: list[OntapApplicationNewIgroup3] = Field(default_factory=list)
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
    s3_bucket_application_components: list[OntapApplicationApplicationComponent2] = Field(
        default_factory=list
    )
    s3_bucket_protection_type_remote_rpo: str = ""
    san_application_components: list[OntapApplicationApplicationComponent3] = Field(
        default_factory=list
    )
    san_exclude_aggregates: list[OntapApplicationExcludeAggregate2] = Field(default_factory=list)
    san_new_igroups: list[OntapApplicationNewIgroup4] = Field(default_factory=list)
    san_os_type: str = ""
    san_protection_type_local_policy: str = ""
    san_protection_type_local_rpo: str = ""
    san_protection_type_remote_rpo: str = ""
    sql_on_san_db_size: int = 0
    sql_on_san_db_storage_service_name: str = ""
    sql_on_san_igroup_name: str = ""
    sql_on_san_log_size: int = 0
    sql_on_san_log_storage_service_name: str = ""
    sql_on_san_new_igroups: list[OntapApplicationNewIgroup5] = Field(default_factory=list)
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
    vdi_on_nas_nfs_access: list[OntapApplicationNfsAccess4] = Field(default_factory=list)
    vdi_on_nas_protection_type_local_rpo: str = ""
    vdi_on_nas_protection_type_remote_rpo: str = ""
    vdi_on_san_desktops_count: int = 0
    vdi_on_san_desktops_size: int = 0
    vdi_on_san_desktops_storage_service_name: str = ""
    vdi_on_san_hypervisor: str = ""
    vdi_on_san_igroup_name: str = ""
    vdi_on_san_new_igroups: list[OntapApplicationNewIgroup6] = Field(default_factory=list)
    vdi_on_san_protection_type_local_rpo: str = ""
    vdi_on_san_protection_type_remote_rpo: str = ""
    vsi_on_nas_datastore_count: int = 0
    vsi_on_nas_datastore_size: int = 0
    vsi_on_nas_datastore_storage_service_name: str = ""
    vsi_on_nas_hyper_v_access_service_account: str = ""
    vsi_on_nas_nfs_access: list[OntapApplicationNfsAccess5] = Field(default_factory=list)
    vsi_on_nas_protection_type_local_rpo: str = ""
    vsi_on_nas_protection_type_remote_rpo: str = ""
    vsi_on_san_datastore_count: int = 0
    vsi_on_san_datastore_size: int = 0
    vsi_on_san_datastore_storage_service_name: str = ""
    vsi_on_san_hypervisor: str = ""
    vsi_on_san_igroup_name: str = ""
    vsi_on_san_new_igroups: list[OntapApplicationNewIgroup7] = Field(default_factory=list)
    vsi_on_san_protection_type_local_rpo: str = ""
    vsi_on_san_protection_type_remote_rpo: str = ""
