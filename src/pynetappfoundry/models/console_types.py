"""Hand-authored compact Console types for cache use.

These classes are intentionally *not* generated — they stay stable across
codegen runs so the cache field types don't change under us. They live
outside ``models/console/``, which ``doit console_models`` clears and
regenerates in full (#825).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from pynetappfoundry.models.console.tenancyv4.get_organizations import (
        Resource10GetResponseBody,
    )


class _ConsoleResource(BaseModel):
    """Fields shared by every tenancyv4 resource (organization, folder, project).

    The spec's GET-by-id responses for these resources share one shape;
    the compact cache types keep only the fields useful for identification.
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


class Organization(_ConsoleResource):
    """Compact view of a Console organization for cache use.

    Hand-authored (not generated) so the cache field type stays stable
    across codegen runs and the cached JSON stays small. Source schema:
    Resource10GetResponseBody in
    pynetappfoundry.models.console.tenancyv4.get_organizations.
    """

    @classmethod
    def from_resource(cls, resource: Resource10GetResponseBody) -> Organization:
        """Convert a generated Resource10GetResponseBody to the compact form.

        Args:
            resource: Generated model from tenancyv4/get_organizations.

        Returns:
            Compact Organization instance.
        """
        return cls.model_validate(resource.model_dump())


class Folder(_ConsoleResource):
    """Compact view of a Console folder for cache use.

    Source schema: the 200 response of ``GET /folders/{folder_id}`` in
    the tenancyv4 spec.
    """


class Project(_ConsoleResource):
    """Compact view of a Console project for cache use.

    Source schema: the 200 response of ``GET /projects/{project_id}`` in
    the tenancyv4 spec.
    """


__all__ = ["Folder", "Organization", "Project"]
