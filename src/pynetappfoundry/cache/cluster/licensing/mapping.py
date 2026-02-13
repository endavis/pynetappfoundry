"""License package type mapping definition for the declarative field mapping framework.

Defines LICENSE_PACKAGE_MAPPING which maps ONTAP REST API license data to
LicensePackage cache model attributes.
"""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.licensing.model import LicenseInstance, LicensePackage
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping


def _api_instances(record: dict[str, Any]) -> list[LicenseInstance]:
    """Transform the nested ``licenses[]`` array into LicenseInstance objects.

    The API returns per-node license instances under the ``licenses`` key.
    Each instance has nested ``capacity.maximum_size`` and
    ``compliance.state`` sub-objects that need flattening.

    Args:
        record: A single license package API record.

    Returns:
        List of LicenseInstance objects parsed from the nested array.
    """
    raw_list = record.get("licenses", [])
    if not isinstance(raw_list, list):
        return []

    instances: list[LicenseInstance] = []
    for entry in raw_list:
        if not isinstance(entry, dict):
            continue
        capacity = entry.get("capacity", {}) or {}
        compliance = entry.get("compliance", {}) or {}
        instances.append(
            LicenseInstance(
                active=entry.get("active", False),
                capacity_max=capacity.get("maximum_size", 0) or 0,
                compliance_state=compliance.get("state", ""),
                evaluation=entry.get("evaluation", False),
                expiry_time=entry.get("expiry_time", ""),
                host_id=entry.get("host_id", ""),
                installed_license=entry.get("installed_license", ""),
                owner=entry.get("owner", ""),
                serial_number=entry.get("serial_number", ""),
                shutdown_imminent=entry.get("shutdown_imminent", False),
                start_time=entry.get("start_time", ""),
            )
        )
    return instances


LICENSE_PACKAGE_MAPPING = TypeMapping(
    name="LicensePackage",
    model_class=LicensePackage,
    api_endpoint="/cluster/licensing/licenses?fields=name,scope,state,description,entitlement,licenses",
    cli_command="",
    fields=(
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="description",
            api_path="description",
        ),
        FieldMapping(
            cache_attr="entitlement_action",
            api_path="entitlement.action",
        ),
        FieldMapping(
            cache_attr="entitlement_risk",
            api_path="entitlement.risk",
        ),
        FieldMapping(
            cache_attr="instances",
            transform=_api_instances,
            default=[],
        ),
    ),
)

model_registry.register_mapping("LicensePackage", LICENSE_PACKAGE_MAPPING)
