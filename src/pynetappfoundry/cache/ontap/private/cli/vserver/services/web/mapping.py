"""OntapSvmWebService type mapping.

Collected through ONTAP's private CLI REST passthrough, the same data as
``vserver services web show -fields vserver,name,enabled``. No public REST
endpoint reports per-service enabled state (#866).
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.private.cli.vserver.services.web.model import (
    OntapSvmWebService,
)

ONTAPSVMWEBSERVICE_MAPPING = TypeMapping(
    name="OntapSvmWebService",
    model_class=OntapSvmWebService,
    api_endpoint="/private/cli/vserver/services/web?fields=vserver,name,enabled",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="vserver",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapSvmWebService", ONTAPSVMWEBSERVICE_MAPPING)
