"""OntapExportRule type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.nfs.export_policies.rules.model import (
    OntapExportRule,
    OntapExportRuleClient,
)


def _transform_clients(record: dict[str, Any]) -> list[OntapExportRuleClient]:
    """Transform clients into OntapExportRuleClient list."""
    return [OntapExportRuleClient(**item) for item in record.get("clients", [])]


ONTAPEXPORTRULE_MAPPING = TypeMapping(
    name="OntapExportRule",
    model_class=OntapExportRule,
    api_endpoint="/protocols/nfs/export-policies/{policy.id}/rules?fields=*",
    api_type="ontap",
    parent_mapping="OntapProtocolsNfsExportPolicy",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="allow_device_creation",
            api_path="allow_device_creation",
            default=False,
        ),
        FieldMapping(
            cache_attr="allow_suid",
            api_path="allow_suid",
            default=False,
        ),
        FieldMapping(
            cache_attr="anonymous_user",
            api_path="anonymous_user",
        ),
        FieldMapping(
            cache_attr="chown_mode",
            api_path="chown_mode",
        ),
        FieldMapping(
            cache_attr="clients",
            transform=_transform_clients,
            default=[],
        ),
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="ntfs_unix_security",
            api_path="ntfs_unix_security",
        ),
        FieldMapping(
            cache_attr="policy_id",
            api_path="policy.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="policy_name",
            api_path="policy.name",
        ),
        FieldMapping(
            cache_attr="protocols",
            api_path="protocols",
            default=[],
        ),
        FieldMapping(
            cache_attr="ro_rule",
            api_path="ro_rule",
            default=[],
        ),
        FieldMapping(
            cache_attr="rw_rule",
            api_path="rw_rule",
            default=[],
        ),
        FieldMapping(
            cache_attr="superuser",
            api_path="superuser",
            default=[],
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapExportRule", ONTAPEXPORTRULE_MAPPING)
