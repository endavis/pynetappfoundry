"""Tests for the hand-authored Console types (`models.console.types`).

These types are intentionally *not* generated — they exist so the cache-side
field types stay stable across codegen runs and the cached JSON stays small.
"""

from __future__ import annotations

from pynetappfoundry.models.console.tenancyv4.get_organizations import (
    Resource10GetResponseBody,
)
from pynetappfoundry.models.console.types import Organization


class TestOrganization:
    """Round-trip and alias behaviour for the compact Organization model."""

    def test_minimal_fields_parse_from_snake_case(self) -> None:
        org = Organization.model_validate(
            {
                "id": "org-abc",
                "name": "Test Org",
                "resource_class": "tenancyv4",
                "resource_type": "organization",
            }
        )
        assert org.id == "org-abc"
        assert org.name == "Test Org"
        assert org.resource_class == "tenancyv4"
        assert org.resource_type == "organization"
        assert org.owner_organization_id is None
        assert org.parent_id is None
        assert org.description is None
        assert org.state is None

    def test_minimal_fields_parse_from_camel_case_alias(self) -> None:
        """populate_by_name=True allows both snake_case and camelCase keys."""
        org = Organization.model_validate(
            {
                "id": "org-abc",
                "name": "Test Org",
                "resourceClass": "tenancyv4",
                "resourceType": "organization",
                "ownerOrganizationId": "owner-xyz",
                "parentId": "parent-456",
            }
        )
        assert org.resource_class == "tenancyv4"
        assert org.resource_type == "organization"
        assert org.owner_organization_id == "owner-xyz"
        assert org.parent_id == "parent-456"

    def test_round_trip_with_by_alias(self) -> None:
        """model_dump(by_alias=True) emits camelCase for cache and wire use."""
        org = Organization.model_validate(
            {
                "id": "org-abc",
                "name": "Test Org",
                "resourceClass": "tenancyv4",
                "resourceType": "organization",
            }
        )
        dumped = org.model_dump(by_alias=True)
        assert dumped["resourceClass"] == "tenancyv4"
        assert dumped["resourceType"] == "organization"

        # And it round-trips back through model_validate
        reparsed = Organization.model_validate(dumped)
        assert reparsed == org

    def test_from_resource_converts_generated_type(self) -> None:
        """from_resource() reduces the generated Resource10GetResponseBody."""
        resource = Resource10GetResponseBody.model_validate(
            {
                "id": "org-from-resource",
                "name": "Generated Org",
                "resourceClass": "tenancyv4",
                "resourceType": "organization",
                "type": "application/vnd.netapp.bxp.resource",
                "version": "1.0",
                "ownerOrganizationId": "owner-9",
                "description": "Pulled from the generator",
                "state": "active",
            }
        )
        org = Organization.from_resource(resource)
        assert org.id == "org-from-resource"
        assert org.name == "Generated Org"
        assert org.resource_class == "tenancyv4"
        assert org.resource_type == "organization"
        assert org.owner_organization_id == "owner-9"
        assert org.description == "Pulled from the generator"
        assert org.state == "active"

    def test_required_field_missing_raises(self) -> None:
        import pydantic

        try:
            Organization.model_validate(
                {"id": "org-x", "name": "X"}
            )  # missing resource_class / resource_type
        except pydantic.ValidationError:
            pass
        else:  # pragma: no cover
            raise AssertionError("expected ValidationError for missing required fields")
