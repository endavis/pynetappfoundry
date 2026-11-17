"""OccmOnpremWorkingEnvironment type mapping (hand-written, ADR-0027).

The fields come from ``ResponseBody.model_fields`` so the mapping cannot drift from the
generated model.  The agent returns the fields in ``EXPLICIT_FETCH_FIELDS`` only when
they are named in ``fields=`` (measured against a lab agent, #1050).
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.console.cvo.get_onprem_working_environments import ResponseBody

EXPLICIT_FETCH_FIELDS: frozenset[str] = frozenset(
    {
        "actionsRequired",
        "capacityFeatures",
        "cbsProperties",
        "cloudSyncProperties",
        "clusterProperties",
        "complianceProperties",
        "cronJobSchedules",
        "interClusterLifs",
        "monitoringProperties",
        "ontapClusterProperties",
        "replicationProperties",
        "reservedSize",
        "snapshotPolicies",
        "status",
        "svms",
    }
)

OCCMONPREMWORKINGENVIRONMENT_MAPPING = TypeMapping(
    name="OccmOnpremWorkingEnvironment",
    model_class=ResponseBody,
    api_endpoint="/occm/api/onprem/working-environments",
    api_type="occm",
    records_path="",
    identifier_field="publicId",
    id_field="name",
    fields=tuple(
        FieldMapping(
            cache_attr=name,
            default=None,
            requires_explicit_fetch=name in EXPLICIT_FETCH_FIELDS,
        )
        for name in ResponseBody.model_fields
    ),
)

model_registry.register_mapping(
    "OccmOnpremWorkingEnvironment", OCCMONPREMWORKINGENVIRONMENT_MAPPING
)
