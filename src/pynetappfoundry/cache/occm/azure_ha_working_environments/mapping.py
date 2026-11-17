"""OccmAzureHaWorkingEnvironment type mapping (hand-written, ADR-0027, #1074).

``GET /occm/api/azure/ha/working-environments`` lists the Azure HA systems.  The
explicit-fetch set is *measured* against live Console agents: only the 8 default keys come
back without ``fields=``.  ``haProperties.node1Info`` and ``haProperties.node2Info``
are present on single-node items too.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.occm._working_environments import build_cloud_we_mapping
from pynetappfoundry.models.console.cvo.get_azure_ha_working_environments import ResponseBody

OCCMAZUREHAWORKINGENVIRONMENT_MAPPING = build_cloud_we_mapping(
    "OccmAzureHaWorkingEnvironment", ResponseBody, "/occm/api/azure/ha/working-environments"
)

model_registry.register_mapping(
    "OccmAzureHaWorkingEnvironment", OCCMAZUREHAWORKINGENVIRONMENT_MAPPING
)
