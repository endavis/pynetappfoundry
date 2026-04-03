"""OntapAwsKms type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.aws_kms.model import (
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
        ),
        FieldMapping(
            cache_attr="amazon_reachability.code",
        ),
        FieldMapping(
            cache_attr="amazon_reachability.message",
        ),
        FieldMapping(
            cache_attr="amazon_reachability.reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="default_domain",
        ),
        FieldMapping(
            cache_attr="ekmip_reachability",
            transform=_transform_ekmip_reachability,
            default=[],
        ),
        FieldMapping(
            cache_attr="encryption_context",
        ),
        FieldMapping(
            cache_attr="host",
        ),
        FieldMapping(
            cache_attr="key_id",
        ),
        FieldMapping(
            cache_attr="polling_period",
            default=0,
        ),
        FieldMapping(
            cache_attr="port",
            default=0,
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
            cache_attr="region",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="secret_access_key",
        ),
        FieldMapping(
            cache_attr="service",
        ),
        FieldMapping(
            cache_attr="skip_verify",
            default=False,
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
            cache_attr="timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="verify",
            default=False,
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

model_registry.register_mapping("OntapAwsKms", ONTAPAWSKMS_MAPPING)
