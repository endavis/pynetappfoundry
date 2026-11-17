"""OccmGcpHaWorkingEnvironment type mapping (hand-written, ADR-0027, #1074).

``GET /occm/api/gcp/ha/working-environments`` lists the GCP HA systems.  The
explicit-fetch set is *inferred*: this list was empty on every measured agent, so it
takes the 8 default keys measured on the other cloud lists.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.occm._working_environments import build_cloud_we_mapping
from pynetappfoundry.models.console.cvo.get_gcp_ha_working_environments import ResponseBody

OCCMGCPHAWORKINGENVIRONMENT_MAPPING = build_cloud_we_mapping(
    "OccmGcpHaWorkingEnvironment", ResponseBody, "/occm/api/gcp/ha/working-environments"
)

model_registry.register_mapping("OccmGcpHaWorkingEnvironment", OCCMGCPHAWORKINGENVIRONMENT_MAPPING)
