"""OntapNvmeInterface type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nvme.interfaces.model import OntapNvmeInterface

ONTAPNVMEINTERFACE_MAPPING = TypeMapping(
    name="OntapNvmeInterface",
    model_class=OntapNvmeInterface,
    api_endpoint="/protocols/nvme/interfaces?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="fc_interface.port.name",
        ),
        FieldMapping(
            cache_attr="fc_interface.port.node.name",
        ),
        FieldMapping(
            cache_attr="fc_interface.port.uuid",
        ),
        FieldMapping(
            cache_attr="fc_interface.wwnn",
        ),
        FieldMapping(
            cache_attr="fc_interface.wwpn",
        ),
        FieldMapping(
            cache_attr="interface_type",
        ),
        FieldMapping(
            cache_attr="ip_interface.ip.address",
        ),
        FieldMapping(
            cache_attr="ip_interface.location.port.name",
        ),
        FieldMapping(
            cache_attr="ip_interface.location.port.node.name",
        ),
        FieldMapping(
            cache_attr="ip_interface.location.port.uuid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="transport_address",
        ),
        FieldMapping(
            cache_attr="transport_protocols",
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNvmeInterface", ONTAPNVMEINTERFACE_MAPPING)
