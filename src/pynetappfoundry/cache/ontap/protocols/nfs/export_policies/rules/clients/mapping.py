"""OntapExportClient type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nfs.export_policies.rules.clients.model import (
    OntapExportClient,
)

ONTAPEXPORTCLIENT_MAPPING = TypeMapping(
    name="OntapExportClient",
    model_class=OntapExportClient,
    api_endpoint="/protocols/nfs/export-policies/{policy.id}/rules/{index}/clients?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="match",
        ),
        FieldMapping(
            cache_attr="policy.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapExportClient", ONTAPEXPORTCLIENT_MAPPING)
