# ruff: noqa: E501
"""OntapApplicationComponent type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.application.applications.components.model import (
    OntapApplicationComponent,
    OntapApplicationComponentBackingStorageLun,
    OntapApplicationComponentBackingStorageNamespace,
    OntapApplicationComponentBackingStorageVolume,
    OntapApplicationComponentCifsAccess,
    OntapApplicationComponentNfsAccess,
    OntapApplicationComponentNvmeAccess,
    OntapApplicationComponentProtectionGroup,
    OntapApplicationComponentSanAccess,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_backing_storage_luns(
    record: dict[str, Any],
) -> list[OntapApplicationComponentBackingStorageLun]:
    """Transform backing_storage.luns into OntapApplicationComponentBackingStorageLun list."""
    try:
        items = get_nested_value(record, "backing_storage.luns")
    except Exception:
        items = []
    return [OntapApplicationComponentBackingStorageLun(**item) for item in items]


def _transform_backing_storage_namespaces(
    record: dict[str, Any],
) -> list[OntapApplicationComponentBackingStorageNamespace]:
    """Transform backing_storage.namespaces into OntapApplicationComponentBackingStorageNamespace list."""
    try:
        items = get_nested_value(record, "backing_storage.namespaces")
    except Exception:
        items = []
    return [OntapApplicationComponentBackingStorageNamespace(**item) for item in items]


def _transform_backing_storage_volumes(
    record: dict[str, Any],
) -> list[OntapApplicationComponentBackingStorageVolume]:
    """Transform backing_storage.volumes into OntapApplicationComponentBackingStorageVolume list."""
    try:
        items = get_nested_value(record, "backing_storage.volumes")
    except Exception:
        items = []
    return [OntapApplicationComponentBackingStorageVolume(**item) for item in items]


def _transform_cifs_access(record: dict[str, Any]) -> list[OntapApplicationComponentCifsAccess]:
    """Transform cifs_access into OntapApplicationComponentCifsAccess list."""
    return [OntapApplicationComponentCifsAccess(**item) for item in record.get("cifs_access", [])]


def _transform_nfs_access(record: dict[str, Any]) -> list[OntapApplicationComponentNfsAccess]:
    """Transform nfs_access into OntapApplicationComponentNfsAccess list."""
    return [OntapApplicationComponentNfsAccess(**item) for item in record.get("nfs_access", [])]


def _transform_nvme_access(record: dict[str, Any]) -> list[OntapApplicationComponentNvmeAccess]:
    """Transform nvme_access into OntapApplicationComponentNvmeAccess list."""
    return [OntapApplicationComponentNvmeAccess(**item) for item in record.get("nvme_access", [])]


def _transform_protection_groups(
    record: dict[str, Any],
) -> list[OntapApplicationComponentProtectionGroup]:
    """Transform protection_groups into OntapApplicationComponentProtectionGroup list."""
    return [
        OntapApplicationComponentProtectionGroup(**item)
        for item in record.get("protection_groups", [])
    ]


def _transform_san_access(record: dict[str, Any]) -> list[OntapApplicationComponentSanAccess]:
    """Transform san_access into OntapApplicationComponentSanAccess list."""
    return [OntapApplicationComponentSanAccess(**item) for item in record.get("san_access", [])]


ONTAPAPPLICATIONCOMPONENT_MAPPING = TypeMapping(
    name="OntapApplicationComponent",
    model_class=OntapApplicationComponent,
    api_endpoint="/application/applications/{application.uuid}/components?fields=*",
    api_type="ontap",
    parent_mapping="OntapApplication",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="application.name",
            api_path="application.name",
        ),
        FieldMapping(
            cache_attr="application.uuid",
            api_path="application.uuid",
        ),
        FieldMapping(
            cache_attr="backing_storage.luns",
            api_path="backing_storage.luns",
            transform=_transform_backing_storage_luns,
            default=[],
        ),
        FieldMapping(
            cache_attr="backing_storage.namespaces",
            api_path="backing_storage.namespaces",
            transform=_transform_backing_storage_namespaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="backing_storage.volumes",
            api_path="backing_storage.volumes",
            transform=_transform_backing_storage_volumes,
            default=[],
        ),
        FieldMapping(
            cache_attr="cifs_access",
            api_path="cifs_access",
            transform=_transform_cifs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="file_system",
            api_path="file_system",
        ),
        FieldMapping(
            cache_attr="host_management_url",
            api_path="host_management_url",
        ),
        FieldMapping(
            cache_attr="host_name",
            api_path="host_name",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="nfs_access",
            api_path="nfs_access",
            transform=_transform_nfs_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="nvme_access",
            api_path="nvme_access",
            transform=_transform_nvme_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="protection_groups",
            api_path="protection_groups",
            transform=_transform_protection_groups,
            default=[],
        ),
        FieldMapping(
            cache_attr="san_access",
            api_path="san_access",
            transform=_transform_san_access,
            default=[],
        ),
        FieldMapping(
            cache_attr="storage_service.name",
            api_path="storage_service.name",
        ),
        FieldMapping(
            cache_attr="storage_service.uuid",
            api_path="storage_service.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapApplicationComponent", ONTAPAPPLICATIONCOMPONENT_MAPPING)
