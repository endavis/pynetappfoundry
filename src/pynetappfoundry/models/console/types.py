"""Hand-authored compact Console types for cache use.

These classes are intentionally *not* generated — they stay stable across
codegen runs so the cache field types don't change under us.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from pynetappfoundry.models.console.tenancyv4.get_organizations import (
        Resource10GetResponseBody,
    )


class Organization(BaseModel):
    """Compact view of a Console organization for cache use.

    Hand-authored (not generated) so the cache field type stays stable
    across codegen runs and the cached JSON stays small. Source schema:
    Resource10GetResponseBody in
    pynetappfoundry.models.console.tenancyv4.get_organizations.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    resource_class: str = Field(alias="resourceClass")
    resource_type: str = Field(alias="resourceType")
    owner_organization_id: str | None = Field(default=None, alias="ownerOrganizationId")
    parent_id: str | None = Field(default=None, alias="parentId")
    description: str | None = None
    state: str | None = None

    @classmethod
    def from_resource(cls, resource: Resource10GetResponseBody) -> Organization:
        """Convert a generated Resource10GetResponseBody to the compact form.

        Args:
            resource: Generated model from tenancyv4/get_organizations.

        Returns:
            Compact Organization instance.
        """
        return cls.model_validate(resource.model_dump())


__all__ = ["Organization"]
