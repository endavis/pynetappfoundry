"""OntapAwsKms type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.security.aws_kms.model import (
    OntapAwsKms,
    OntapAwsKmsEkmipReachability,
)


def _transform_ekmip_reachability(record: dict[str, Any]) -> list[OntapAwsKmsEkmipReachability]:
    """Transform ekmip_reachability into OntapAwsKmsEkmipReachability list."""
    return [OntapAwsKmsEkmipReachability(**item) for item in record.get("ekmip_reachability", [])]


ONTAPAWSKMS_MAPPING = TypeMapping(
    name="OntapAwsKms",
    model_class=OntapAwsKms,
    api_endpoint="/security/aws-kms?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="access_key_id",
            api_path="access_key_id",
        ),
        FieldMapping(
            cache_attr="amazon_reachability_code",
            api_path="amazon_reachability.code",
        ),
        FieldMapping(
            cache_attr="amazon_reachability_message",
            api_path="amazon_reachability.message",
        ),
        FieldMapping(
            cache_attr="amazon_reachability_reachable",
            api_path="amazon_reachability.reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="default_domain",
            api_path="default_domain",
        ),
        FieldMapping(
            cache_attr="ekmip_reachability",
            transform=_transform_ekmip_reachability,
            default=[],
        ),
        FieldMapping(
            cache_attr="encryption_context",
            api_path="encryption_context",
        ),
        FieldMapping(
            cache_attr="host",
            api_path="host",
        ),
        FieldMapping(
            cache_attr="key_id",
            api_path="key_id",
        ),
        FieldMapping(
            cache_attr="polling_period",
            api_path="polling_period",
            default=0,
        ),
        FieldMapping(
            cache_attr="port",
            api_path="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="proxy_host",
            api_path="proxy_host",
        ),
        FieldMapping(
            cache_attr="proxy_password",
            api_path="proxy_password",
        ),
        FieldMapping(
            cache_attr="proxy_port",
            api_path="proxy_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="proxy_type",
            api_path="proxy_type",
        ),
        FieldMapping(
            cache_attr="proxy_username",
            api_path="proxy_username",
        ),
        FieldMapping(
            cache_attr="region",
            api_path="region",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="secret_access_key",
            api_path="secret_access_key",
        ),
        FieldMapping(
            cache_attr="service",
            api_path="service",
        ),
        FieldMapping(
            cache_attr="skip_verify",
            api_path="skip_verify",
            default=False,
        ),
        FieldMapping(
            cache_attr="state_cluster_state",
            api_path="state.cluster_state",
            default=False,
        ),
        FieldMapping(
            cache_attr="state_code",
            api_path="state.code",
        ),
        FieldMapping(
            cache_attr="state_message",
            api_path="state.message",
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
            cache_attr="timeout",
            api_path="timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="verify",
            api_path="verify",
            default=False,
        ),
        FieldMapping(
            cache_attr="verify_host",
            api_path="verify_host",
            default=False,
        ),
        FieldMapping(
            cache_attr="verify_ip",
            api_path="verify_ip",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapAwsKms", ONTAPAWSKMS_MAPPING)
