"""OntapNvmeInterface type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.nvme.interfaces.model import OntapNvmeInterface

ONTAPNVMEINTERFACE_MAPPING = TypeMapping(
    name="OntapNvmeInterface",
    model_class=OntapNvmeInterface,
    api_endpoint="/protocols/nvme/interfaces?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="fc_interface_port_name",
            api_path="fc_interface.port.name",
        ),
        FieldMapping(
            cache_attr="fc_interface_port_node_name",
            api_path="fc_interface.port.node.name",
        ),
        FieldMapping(
            cache_attr="fc_interface_port_uuid",
            api_path="fc_interface.port.uuid",
        ),
        FieldMapping(
            cache_attr="fc_interface_wwnn",
            api_path="fc_interface.wwnn",
        ),
        FieldMapping(
            cache_attr="fc_interface_wwpn",
            api_path="fc_interface.wwpn",
        ),
        FieldMapping(
            cache_attr="interface_type",
            api_path="interface_type",
        ),
        FieldMapping(
            cache_attr="ip_interface_ip_address",
            api_path="ip_interface.ip.address",
        ),
        FieldMapping(
            cache_attr="ip_interface_location_port_name",
            api_path="ip_interface.location.port.name",
        ),
        FieldMapping(
            cache_attr="ip_interface_location_port_node_name",
            api_path="ip_interface.location.port.node.name",
        ),
        FieldMapping(
            cache_attr="ip_interface_location_port_uuid",
            api_path="ip_interface.location.port.uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="transport_address",
            api_path="transport_address",
        ),
        FieldMapping(
            cache_attr="transport_protocols",
            api_path="transport_protocols",
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNvmeInterface", ONTAPNVMEINTERFACE_MAPPING)
