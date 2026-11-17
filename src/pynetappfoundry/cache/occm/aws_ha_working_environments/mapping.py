"""OccmAwsHaWorkingEnvironment type mapping (hand-written, ADR-0027, #1074).

``GET /occm/api/aws/ha/working-environments`` lists the AWS HA systems.  The
explicit-fetch set is *measured* against live Console agents: only the 8 default keys come
back without ``fields=`` (see ``pynetappfoundry.cache.occm._working_environments``).
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.occm._working_environments import build_cloud_we_mapping
from pynetappfoundry.models.console.cvo.get_aws_ha_working_environments import ResponseBody

OCCMAWSHAWORKINGENVIRONMENT_MAPPING = build_cloud_we_mapping(
    "OccmAwsHaWorkingEnvironment", ResponseBody, "/occm/api/aws/ha/working-environments"
)

model_registry.register_mapping("OccmAwsHaWorkingEnvironment", OCCMAWSHAWORKINGENVIRONMENT_MAPPING)
