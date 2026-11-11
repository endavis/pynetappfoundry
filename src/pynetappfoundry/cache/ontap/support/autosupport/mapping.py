"""OntapAutosupport type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.autosupport.model import (
    OntapAutosupport,
    OntapAutosupportIssue,
)

ONTAPAUTOSUPPORT_MAPPING = TypeMapping(
    name="OntapAutosupport",
    model_class=OntapAutosupport,
    api_endpoint="/support/autosupport?fields=*",
    api_type="ontap",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="contact_support",
            default=False,
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="from_",
            api_path="from",
        ),
        FieldMapping(
            cache_attr="is_minimal",
            default=False,
        ),
        FieldMapping(
            cache_attr="issues",
            item_model=OntapAutosupportIssue,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="mail_hosts",
            default=[],
        ),
        FieldMapping(
            cache_attr="ondemand_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="partner_addresses",
            default=[],
        ),
        FieldMapping(
            cache_attr="proxy_url",
        ),
        FieldMapping(
            cache_attr="smtp_encryption",
        ),
        FieldMapping(
            cache_attr="to",
            default=[],
        ),
        FieldMapping(
            cache_attr="transport",
        ),
    ),
)

model_registry.register_mapping("OntapAutosupport", ONTAPAUTOSUPPORT_MAPPING)
