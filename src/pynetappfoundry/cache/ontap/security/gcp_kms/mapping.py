"""OntapGcpKms type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.gcp_kms.model import (
    OntapGcpKms,
    OntapGcpKmsEkmipReachability,
)


def _transform_ekmip_reachability(record: dict[str, Any]) -> list[OntapGcpKmsEkmipReachability]:
    """Transform ekmip_reachability into OntapGcpKmsEkmipReachability list."""
    return [OntapGcpKmsEkmipReachability(**item) for item in record.get("ekmip_reachability", [])]


ONTAPGCPKMS_MAPPING = TypeMapping(
    name="OntapGcpKms",
    model_class=OntapGcpKms,
    api_endpoint="/security/gcp-kms?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="application_credentials",
        ),
        FieldMapping(
            cache_attr="caller_account",
        ),
        FieldMapping(
            cache_attr="cloudkms_host",
        ),
        FieldMapping(
            cache_attr="ekmip_reachability",
            transform=_transform_ekmip_reachability,
            default=[],
        ),
        FieldMapping(
            cache_attr="google_reachability.code",
        ),
        FieldMapping(
            cache_attr="google_reachability.message",
        ),
        FieldMapping(
            cache_attr="google_reachability.reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="key_name",
        ),
        FieldMapping(
            cache_attr="key_ring_location",
        ),
        FieldMapping(
            cache_attr="key_ring_name",
        ),
        FieldMapping(
            cache_attr="oauth_host",
        ),
        FieldMapping(
            cache_attr="oauth_url",
        ),
        FieldMapping(
            cache_attr="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="privileged_account",
        ),
        FieldMapping(
            cache_attr="project_id",
        ),
        FieldMapping(
            cache_attr="proxy_host",
        ),
        FieldMapping(
            cache_attr="proxy_password",
        ),
        FieldMapping(
            cache_attr="proxy_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="proxy_type",
        ),
        FieldMapping(
            cache_attr="proxy_username",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="state.cluster_state",
            default=False,
        ),
        FieldMapping(
            cache_attr="state.code",
        ),
        FieldMapping(
            cache_attr="state.message",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="verify_host",
            default=False,
        ),
        FieldMapping(
            cache_attr="verify_ip",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapGcpKms", ONTAPGCPKMS_MAPPING)
