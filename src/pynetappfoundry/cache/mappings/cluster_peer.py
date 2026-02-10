"""ClusterPeer type mapping definition for the declarative field mapping framework.

Defines CLUSTER_PEER_MAPPING which maps ONTAP REST API cluster peer data
to ClusterPeer cache model attributes. ClusterPeer is API-only — there is
no CLI command for this data.

The ``remote`` and ``authentication`` fields can be either dicts or strings
depending on the ONTAP API version, so transform functions handle both
shapes safely.
"""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.models import ClusterPeer


def _api_remote_cluster_name(record: dict[str, Any]) -> str:
    """Extract remote cluster name from API response.

    Handles API version differences where ``remote`` can be a dict
    (with a ``name`` key) or a plain string.

    Args:
        record: Full API cluster peer record.

    Returns:
        Remote cluster name string.
    """
    remote = record.get("remote")
    if isinstance(remote, dict):
        return str(remote.get("name", ""))
    return str(remote or "")


def _api_peer_addresses(record: dict[str, Any]) -> list[str]:
    """Extract peer IP addresses from API response.

    Extracts ``remote.ip_addresses`` when ``remote`` is a dict,
    filtering out empty/falsy values.

    Args:
        record: Full API cluster peer record.

    Returns:
        List of non-empty peer IP address strings.
    """
    remote = record.get("remote")
    if isinstance(remote, dict):
        return [addr for addr in remote.get("ip_addresses", []) if addr]
    return []


def _api_authentication_state(record: dict[str, Any]) -> str:
    """Extract authentication state from API response.

    Handles API version differences where ``authentication`` can be a
    dict (with a ``state`` key) or a plain string.

    Args:
        record: Full API cluster peer record.

    Returns:
        Authentication state string.
    """
    auth = record.get("authentication")
    if isinstance(auth, dict):
        return str(auth.get("state", ""))
    return str(auth or "")


def _api_authentication_in_use(record: dict[str, Any]) -> str:
    """Extract authentication method in use from API response.

    Args:
        record: Full API cluster peer record.

    Returns:
        Authentication method in use string.
    """
    auth = record.get("authentication")
    if isinstance(auth, dict):
        return str(auth.get("in_use", ""))
    return ""


def _api_encryption_state(record: dict[str, Any]) -> str:
    """Extract encryption state from API response.

    Args:
        record: Full API cluster peer record.

    Returns:
        Encryption state string.
    """
    encryption = record.get("encryption")
    if isinstance(encryption, dict):
        return str(encryption.get("state", ""))
    return str(encryption or "")


CLUSTER_PEER_MAPPING = TypeMapping(
    name="ClusterPeer",
    model_class=ClusterPeer,
    api_endpoint="/cluster/peers?fields=*",
    cli_command="",
    fields=(
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="remote_cluster_name",
            transform=_api_remote_cluster_name,
        ),
        FieldMapping(
            cache_attr="peer_addresses",
            default=[],
            transform=_api_peer_addresses,
        ),
        FieldMapping(
            cache_attr="authentication_state",
            transform=_api_authentication_state,
        ),
        FieldMapping(
            cache_attr="authentication_in_use",
            transform=_api_authentication_in_use,
        ),
        FieldMapping(
            cache_attr="encryption_state",
            transform=_api_encryption_state,
        ),
    ),
)
