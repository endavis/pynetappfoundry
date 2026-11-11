"""OntapApplicationComponent type mapping."""

from __future__ import annotations

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
        ),
        FieldMapping(
            cache_attr="application.uuid",
        ),
        FieldMapping(
            cache_attr="backing_storage.luns",
            item_model=OntapApplicationComponentBackingStorageLun,
            default=[],
        ),
        FieldMapping(
            cache_attr="backing_storage.namespaces",
            item_model=OntapApplicationComponentBackingStorageNamespace,
            default=[],
        ),
        FieldMapping(
            cache_attr="backing_storage.volumes",
            item_model=OntapApplicationComponentBackingStorageVolume,
            default=[],
        ),
        FieldMapping(
            cache_attr="cifs_access",
            item_model=OntapApplicationComponentCifsAccess,
            default=[],
        ),
        FieldMapping(
            cache_attr="file_system",
        ),
        FieldMapping(
            cache_attr="host_management_url",
        ),
        FieldMapping(
            cache_attr="host_name",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="nfs_access",
            item_model=OntapApplicationComponentNfsAccess,
            default=[],
        ),
        FieldMapping(
            cache_attr="nvme_access",
            item_model=OntapApplicationComponentNvmeAccess,
            default=[],
        ),
        FieldMapping(
            cache_attr="protection_groups",
            item_model=OntapApplicationComponentProtectionGroup,
            default=[],
        ),
        FieldMapping(
            cache_attr="san_access",
            item_model=OntapApplicationComponentSanAccess,
            default=[],
        ),
        FieldMapping(
            cache_attr="storage_service.name",
        ),
        FieldMapping(
            cache_attr="storage_service.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapApplicationComponent", ONTAPAPPLICATIONCOMPONENT_MAPPING)
