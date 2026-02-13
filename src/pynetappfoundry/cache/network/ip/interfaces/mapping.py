"""NetworkLIF type mapping definition for the declarative field mapping framework.

Defines NETWORK_LIF_MAPPING which maps ONTAP REST API network IP interface
data to NetworkLIF cache model attributes. NetworkLIF is API-only --
there is no CLI command for this data.

All fields use simple dot-path extraction; no transform functions are needed.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.network.ip.interfaces.model import NetworkLIF

NETWORK_LIF_MAPPING = TypeMapping(
    name="NetworkLIF",
    model_class=NetworkLIF,
    api_endpoint="/network/ip/interfaces?fields=*",
    cli_command="",
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
            cache_attr="ip_address",
            api_path="ip.address",
        ),
        FieldMapping(
            cache_attr="netmask",
            api_path="ip.netmask",
        ),
        FieldMapping(
            cache_attr="ip_family",
            api_path="ip.family",
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=True,
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="vip",
            api_path="vip",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="ipspace_uuid",
            api_path="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="service_policy_uuid",
            api_path="service_policy.uuid",
        ),
        FieldMapping(
            cache_attr="services",
            api_path="services",
            default=[],
        ),
        FieldMapping(
            cache_attr="auto_revert",
            api_path="location.auto_revert",
            default=False,
        ),
        FieldMapping(
            cache_attr="failover",
            api_path="location.failover",
        ),
        FieldMapping(
            cache_attr="is_home",
            api_path="location.is_home",
            default=True,
        ),
        FieldMapping(
            cache_attr="home_node_uuid",
            api_path="location.home_node.uuid",
        ),
        FieldMapping(
            cache_attr="home_port_uuid",
            api_path="location.home_port.uuid",
        ),
        FieldMapping(
            cache_attr="current_node_uuid",
            api_path="location.node.uuid",
        ),
        FieldMapping(
            cache_attr="current_port_uuid",
            api_path="location.port.uuid",
        ),
        FieldMapping(
            cache_attr="dns_zone",
            api_path="dns_zone",
        ),
        FieldMapping(
            cache_attr="ddns_enabled",
            api_path="ddns_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="subnet_uuid",
            api_path="subnet.uuid",
        ),
        FieldMapping(
            cache_attr="probe_port",
            api_path="probe_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="rdma_protocols",
            api_path="rdma_protocols",
            default=[],
        ),
    ),
)

model_registry.register_mapping("NetworkLIF", NETWORK_LIF_MAPPING)
