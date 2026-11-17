"""OccmAwsWorkingEnvironment type mapping (hand-written, ADR-0027, #1074).

``GET /occm/api/vsa/working-environments`` lists the AWS single-node systems.  The
explicit-fetch set is *inferred*: this list was empty on every measured agent, so it
takes the 8 default keys measured on the other cloud lists (see
``pynetappfoundry.cache.occm._working_environments``).
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.occm._working_environments import build_cloud_we_mapping
from pynetappfoundry.models.console.cvo.get_vsa_working_environments import ResponseBody

OCCMAWSWORKINGENVIRONMENT_MAPPING = build_cloud_we_mapping(
    "OccmAwsWorkingEnvironment", ResponseBody, "/occm/api/vsa/working-environments"
)

model_registry.register_mapping("OccmAwsWorkingEnvironment", OCCMAWSWORKINGENVIRONMENT_MAPPING)
