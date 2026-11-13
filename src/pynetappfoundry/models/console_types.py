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
    from pynetappfoundry.models.console.cvo import get_occm_system_about
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


class ConnectorSiteIdentifier(BaseModel):
    """Site identification of a Console agent (connector).

    Only ``company`` and ``site`` are kept.  The agent's ``host`` is a network
    address and is not persisted in the cache.
    """

    company: str | None = None
    site: str | None = None


class Connector(BaseModel):
    """Compact view of a Console agent (connector) for cache use.

    Source schema: the 200 response of ``GET /occm/api/occm/system/about`` in
    the Console agent (cvo) spec.  Network addresses (``privateIp``,
    ``siteIdentifier.host``) are dropped on validation so they never reach
    the cache.
    """

    model_config = ConfigDict(populate_by_name=True)

    agent_id: str = Field(alias="agentId")
    version: str | None = None
    system_id: str | None = Field(default=None, alias="systemId")
    environment: str | None = None
    agent_type: str | None = Field(default=None, alias="agentType")
    site_identifier: ConnectorSiteIdentifier | None = Field(default=None, alias="siteIdentifier")

    @classmethod
    def from_about(
        cls, about: get_occm_system_about.ResponseBody, *, agent_id: str | None = None
    ) -> Connector:
        """Convert a generated about response to the compact form.

        Args:
            about: Generated model from cvo/get_occm_system_about.
            agent_id: Agent id to use when the response carries none.

        Returns:
            Compact Connector instance.

        Raises:
            pydantic.ValidationError: If neither the response nor ``agent_id``
                provides an agent id.
        """
        data = about.model_dump()
        if data.get("agentId") is None:
            data["agentId"] = agent_id
        return cls.model_validate(data)


__all__ = ["Connector", "ConnectorSiteIdentifier", "Folder", "Organization", "Project"]
