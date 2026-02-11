"""Node type mapping definition for the declarative field mapping framework.

Defines NODE_MAPPING which maps ONTAP REST API and CLI node data to
NodeInfo cache model attributes.
"""

from __future__ import annotations

from pynetappfoundry.cache.cluster.nodes.model import NodeInfo
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

NODE_MAPPING = TypeMapping(
    name="Node",
    model_class=NodeInfo,
    api_endpoint="/cluster/nodes?fields=*",
    cli_command="system node show",
    fields=(
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="serial_number",
            api_path="serial_number",
        ),
        FieldMapping(
            cache_attr="system_id",
            api_path="system_id",
        ),
        FieldMapping(
            cache_attr="model",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="location",
            api_path="location",
        ),
        FieldMapping(
            cache_attr="membership",
            api_path="membership",
        ),
        FieldMapping(
            cache_attr="version_full",
            api_path="version.full",
        ),
        FieldMapping(
            cache_attr="storage_configuration",
            api_path="storage_configuration",
        ),
        FieldMapping(
            cache_attr="system_machine_type",
            api_path="system_machine_type",
        ),
        FieldMapping(
            cache_attr="controller_board",
            api_path="controller.board",
        ),
        FieldMapping(
            cache_attr="controller_memory_size",
            api_path="controller.memory_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller_cpu_count",
            api_path="controller.cpu.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="vm_provider_type",
            api_path="vm.provider_type",
        ),
        FieldMapping(
            cache_attr="ha_enabled",
            api_path="ha.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="ha_auto_giveback",
            api_path="ha.auto_giveback",
            default=False,
        ),
        FieldMapping(
            cache_attr="ha_partner_uuids",
            api_path="ha.partners[*].uuid",
            default=[],
        ),
        FieldMapping(
            cache_attr="system_aggregate_uuid",
            api_path="system_aggregate.uuid",
        ),
        FieldMapping(
            cache_attr="cluster_interface_uuids",
            api_path="cluster_interfaces[*].uuid",
            default=[],
        ),
        FieldMapping(
            cache_attr="management_interface_uuids",
            api_path="management_interfaces[*].uuid",
            default=[],
        ),
    ),
)
