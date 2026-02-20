"""OntapExportPolicy type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.nfs.export_policies.model import (
    OntapExportPolicy,
    OntapExportPolicyClient,
)


def _transform_clients(record: dict[str, Any]) -> list[OntapExportPolicyClient]:
    """Transform clients into OntapExportPolicyClient list."""
    return [OntapExportPolicyClient(**item) for item in record.get("clients", [])]


ONTAPEXPORTPOLICY_MAPPING = TypeMapping(
    name="OntapExportPolicy",
    model_class=OntapExportPolicy,
    api_endpoint="/protocols/nfs/export-policies?fields=*",
    api_type="ontap",
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
    ),
)

model_registry.register_mapping("OntapExportPolicy", ONTAPEXPORTPOLICY_MAPPING)
