"""OccmAzureWorkingEnvironment type mapping (hand-written, ADR-0027, #1074).

``GET /occm/api/azure/vsa/working-environments`` lists the Azure single-node systems.
The explicit-fetch set is *measured* against live Console agents: only the 8 default keys come
back without ``fields=``.  Single-node items also carry ``haProperties.node1Info`` and
``haProperties.node2Info``.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.occm._working_environments import build_cloud_we_mapping
from pynetappfoundry.models.console.cvo.get_azure_vsa_working_environments import ResponseBody

OCCMAZUREWORKINGENVIRONMENT_MAPPING = build_cloud_we_mapping(
    "OccmAzureWorkingEnvironment", ResponseBody, "/occm/api/azure/vsa/working-environments"
)

model_registry.register_mapping("OccmAzureWorkingEnvironment", OCCMAZUREWORKINGENVIRONMENT_MAPPING)
