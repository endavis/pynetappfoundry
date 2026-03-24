"""OntapCifsDomain type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.cifs.domains.model import (
    OntapCifsDomain,
    OntapCifsDomainDiscoveredServer,
    OntapCifsDomainPreferredDc,
    OntapCifsDomainTrustRelationship,
)


def _transform_discovered_servers(record: dict[str, Any]) -> list[OntapCifsDomainDiscoveredServer]:
    """Transform discovered_servers into OntapCifsDomainDiscoveredServer list."""
    return [
        OntapCifsDomainDiscoveredServer(**item) for item in record.get("discovered_servers", [])
    ]


def _transform_preferred_dcs(record: dict[str, Any]) -> list[OntapCifsDomainPreferredDc]:
    """Transform preferred_dcs into OntapCifsDomainPreferredDc list."""
    return [OntapCifsDomainPreferredDc(**item) for item in record.get("preferred_dcs", [])]


def _transform_trust_relationships(
    record: dict[str, Any],
) -> list[OntapCifsDomainTrustRelationship]:
    """Transform trust_relationships into OntapCifsDomainTrustRelationship list."""
    return [
        OntapCifsDomainTrustRelationship(**item) for item in record.get("trust_relationships", [])
    ]


ONTAPCIFSDOMAIN_MAPPING = TypeMapping(
    name="OntapCifsDomain",
    model_class=OntapCifsDomain,
    api_endpoint="/protocols/cifs/domains?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="ad_domain_password",
            api_path="ad_domain.password",
        ),
        FieldMapping(
            cache_attr="ad_domain_user",
            api_path="ad_domain.user",
        ),
        FieldMapping(
            cache_attr="client_certificate",
            api_path="client_certificate",
        ),
        FieldMapping(
            cache_attr="client_id",
            api_path="client_id",
        ),
        FieldMapping(
            cache_attr="discovered_servers",
            api_path="discovered_servers",
            transform=_transform_discovered_servers,
            default=[],
        ),
        FieldMapping(
            cache_attr="name_mapping_trusted_domains",
            api_path="name_mapping.trusted_domains",
            default=[],
        ),
        FieldMapping(
            cache_attr="password_schedule_schedule_day_of_week",
            api_path="password_schedule.schedule_day_of_week",
        ),
        FieldMapping(
            cache_attr="password_schedule_schedule_description",
            api_path="password_schedule.schedule_description",
        ),
        FieldMapping(
            cache_attr="password_schedule_schedule_enabled",
            api_path="password_schedule.schedule_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="password_schedule_schedule_last_changed_time",
            api_path="password_schedule.schedule_last_changed_time",
        ),
        FieldMapping(
            cache_attr="password_schedule_schedule_randomized_minute",
            api_path="password_schedule.schedule_randomized_minute",
            default=0,
        ),
        FieldMapping(
            cache_attr="password_schedule_schedule_time_of_day",
            api_path="password_schedule.schedule_time_of_day",
        ),
        FieldMapping(
            cache_attr="password_schedule_schedule_warn_message",
            api_path="password_schedule.schedule_warn_message",
        ),
        FieldMapping(
            cache_attr="password_schedule_schedule_weekly_interval",
            api_path="password_schedule.schedule_weekly_interval",
            default=0,
        ),
        FieldMapping(
            cache_attr="preferred_dcs",
            api_path="preferred_dcs",
            transform=_transform_preferred_dcs,
            default=[],
        ),
        FieldMapping(
            cache_attr="server_discovery_mode",
            api_path="server_discovery_mode",
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
            cache_attr="tenant_id",
            api_path="tenant_id",
        ),
        FieldMapping(
            cache_attr="trust_relationships",
            api_path="trust_relationships",
            transform=_transform_trust_relationships,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapCifsDomain", ONTAPCIFSDOMAIN_MAPPING)
