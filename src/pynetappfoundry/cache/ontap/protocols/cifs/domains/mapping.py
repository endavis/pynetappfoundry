"""OntapCifsDomain type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.domains.model import (
    OntapCifsDomain,
    OntapCifsDomainDiscoveredServer,
    OntapCifsDomainPreferredDc,
    OntapCifsDomainTrustRelationship,
)

ONTAPCIFSDOMAIN_MAPPING = TypeMapping(
    name="OntapCifsDomain",
    model_class=OntapCifsDomain,
    api_endpoint="/protocols/cifs/domains?fields=*",
    api_type="ontap",
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="ad_domain.password",
        ),
        FieldMapping(
            cache_attr="ad_domain.user",
        ),
        FieldMapping(
            cache_attr="client_certificate",
        ),
        FieldMapping(
            cache_attr="client_id",
        ),
        FieldMapping(
            cache_attr="discovered_servers",
            item_model=OntapCifsDomainDiscoveredServer,
            default=[],
        ),
        FieldMapping(
            cache_attr="name_mapping.trusted_domains",
            default=[],
        ),
        FieldMapping(
            cache_attr="password_schedule.schedule_day_of_week",
        ),
        FieldMapping(
            cache_attr="password_schedule.schedule_description",
        ),
        FieldMapping(
            cache_attr="password_schedule.schedule_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="password_schedule.schedule_last_changed_time",
        ),
        FieldMapping(
            cache_attr="password_schedule.schedule_randomized_minute",
            default=0,
        ),
        FieldMapping(
            cache_attr="password_schedule.schedule_time_of_day",
        ),
        FieldMapping(
            cache_attr="password_schedule.schedule_warn_message",
        ),
        FieldMapping(
            cache_attr="password_schedule.schedule_weekly_interval",
            default=0,
        ),
        FieldMapping(
            cache_attr="preferred_dcs",
            item_model=OntapCifsDomainPreferredDc,
            default=[],
        ),
        FieldMapping(
            cache_attr="server_discovery_mode",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="tenant_id",
        ),
        FieldMapping(
            cache_attr="trust_relationships",
            item_model=OntapCifsDomainTrustRelationship,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapCifsDomain", ONTAPCIFSDOMAIN_MAPPING)
