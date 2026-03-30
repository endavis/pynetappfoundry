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
    parent_mapping=None,
    parent_id_field=None,
    fields=(
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="match",
            api_path="match",
        ),
        FieldMapping(
            cache_attr="policy_id",
            api_path="policy.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapExportClient", ONTAPEXPORTCLIENT_MAPPING)
