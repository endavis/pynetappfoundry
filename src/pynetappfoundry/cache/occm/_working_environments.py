"""Shared builder for the cloud working-environment mappings (#1074, ADR-0027).

Every cloud list returns the same 8 keys by default (measured on AWS HA, Azure single
node and Azure HA against live Console agents); every other field is returned only when it is
named in ``fields=``.  The on-prem mapping keeps its own measured set.
"""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

#: The keys a cloud working-environment list returns without ``fields=``.
DEFAULT_FIELDS: frozenset[str] = frozenset(
    {
        "cloudProviderName",
        "creatorUserEmail",
        "isHA",
        "name",
        "publicId",
        "svmName",
        "tenantId",
        "workingEnvironmentType",
    }
)


def build_cloud_we_mapping(name: str, model_class: type[Any], api_endpoint: str) -> TypeMapping:
    """Build the mapping of one cloud working-environment list.

    Args:
        name: The mapping name.
        model_class: The generated ``ResponseBody`` of the list op.
        api_endpoint: The list endpoint path.

    Returns:
        A mapping with one field per model field; all but ``DEFAULT_FIELDS`` are
        ``requires_explicit_fetch``.
    """
    return TypeMapping(
        name=name,
        model_class=model_class,
        api_endpoint=api_endpoint,
        api_type="occm",
        records_path="",
        identifier_field="publicId",
        id_field="name",
        fields=tuple(
            FieldMapping(
                cache_attr=field_name,
                default=None,
                requires_explicit_fetch=field_name not in DEFAULT_FIELDS,
            )
            for field_name in model_class.model_fields
        ),
    )
