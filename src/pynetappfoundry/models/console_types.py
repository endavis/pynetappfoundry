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
    from pynetappfoundry.models.console.agentsmgmt import get_agent, get_list_connectors
    from pynetappfoundry.models.console.cvo import (
        get_occm_saas_mp_service_account,
        get_occm_system_about,
    )
    from pynetappfoundry.models.console.dw import get_license_account_subscriptions_preferred
    from pynetappfoundry.models.console.tenancyv4 import get_organizations_resources
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


class MarketplaceSubscription(BaseModel):
    """Compact view of a SaaS marketplace subscription of the Console account.

    Source schema: ``SubscriptionResponse`` items in the 200 response of
    ``GET /occm/api/occm/saas-mp-service/account`` in the Console agent (cvo)
    spec.  Cloud account IDs and free-trial flags are dropped.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str | None = None
    provider: str | None = None
    active: bool | None = None
    contract: bool | None = None
    by_node_mode: bool | None = Field(default=None, alias="byNodeMode")
    eligible_cvo_packages: list[str] = Field(default_factory=list, alias="eligibleCvoPackages")

    @classmethod
    def from_account(
        cls, body: get_occm_saas_mp_service_account.ResponseBody
    ) -> list[MarketplaceSubscription]:
        """Flatten the per-provider subscription lists of an account response.

        Args:
            body: Generated model from cvo/get_occm_saas_mp_service_account.

        Returns:
            Subscriptions in aws, azure, gcp order.  A missing ``provider`` is
            filled from the list the item came from.

        Raises:
            pydantic.ValidationError: If a subscription has no ``id``.
        """
        groups = (
            ("aws", body.awsSubscriptions),
            ("azure", body.azureSubscriptions),
            ("gcp", body.gcpSubscriptions),
        )
        result: list[MarketplaceSubscription] = []
        for provider, items in groups:
            for item in items or []:
                data = item.model_dump()
                if data.get("provider") is None:
                    data["provider"] = provider
                if data.get("eligibleCvoPackages") is None:
                    data["eligibleCvoPackages"] = []
                result.append(cls.model_validate(data))
        return result


class SubscriptionEntitlement(BaseModel):
    """Compact view of one entitlement of an account subscription (#1034).

    Source schema: ``entitlements.items`` of the preferred-subscription response
    of ``GET /license/account/{accountId}/subscriptions/preferred`` in the Console
    ``dw`` spec.  The fields come from the docs, not from a live response.
    """

    model_config = ConfigDict(populate_by_name=True)

    contract_option: str | None = Field(default=None, alias="contractOption")
    units: str | None = None
    expiration_date: str | None = Field(default=None, alias="expirationDate")
    category: str | None = None
    dimension: str | None = None
    unit: str | None = None
    service_name: str | None = Field(default=None, alias="serviceName")


class AccountSubscription(BaseModel):
    """Compact view of one preferred subscription of a Console account (#1034).

    Source schema: an item of the 200 response of
    ``GET /license/account/{accountId}/subscriptions/preferred`` in the Console
    ``dw`` spec.  Cloud account IDs (``cloudIds``), ``customerIdentifier``,
    ``listingUrl`` and the other display fields are dropped.  The item fields come
    from the docs; the live response was an empty array.
    """

    model_config = ConfigDict(populate_by_name=True)

    subscription_id: str = Field(alias="subscriptionId")
    subscription_name: str | None = Field(default=None, alias="subscriptionName")
    subscription_status: str | None = Field(default=None, alias="subscriptionStatus")
    service_name: str | None = Field(default=None, alias="serviceName")
    cloud_provider: str | None = Field(default=None, alias="cloudProvider")
    plan_id: str | None = Field(default=None, alias="planId")
    product_code: str | None = Field(default=None, alias="productCode")
    contract: bool | None = None
    auto_renew: str | None = Field(default=None, alias="autoRenew")
    end_date: int | None = Field(default=None, alias="endDate")
    """End of the subscription as epoch milliseconds, as documented."""
    term: str | None = None
    accounts: list[str] = Field(default_factory=list)
    entitlements: list[SubscriptionEntitlement] = Field(default_factory=list)

    @classmethod
    def from_preferred(
        cls, body: get_license_account_subscriptions_preferred.Response200Body
    ) -> AccountSubscription:
        """Build from one item of the preferred-subscriptions response.

        Args:
            body: Generated model from dw/get_license_account_subscriptions_preferred.

        Returns:
            The compact subscription; a missing entitlements block gives ``[]``.

        Raises:
            pydantic.ValidationError: If the item has no ``subscriptionId``.
        """
        data = body.model_dump(
            include={
                "subscriptionId",
                "subscriptionName",
                "subscriptionStatus",
                "serviceName",
                "cloudProvider",
                "planId",
                "productCode",
                "contract",
                "autoRenew",
                "endDate",
                "term",
                "accounts",
            }
        )
        if data.get("accounts") is None:
            data["accounts"] = []
        items = body.entitlements.items if body.entitlements is not None else None
        data["entitlements"] = [item.model_dump() for item in items or []]
        return cls.model_validate(data)


class ConsoleAgentInfo(BaseModel):
    """Compact view of a Console agent found by discovery (#1078).

    Source schemas: the ``Agent`` of an ``Occm`` in the response of
    ``GET /agents-mgmt/list-connectors/{organization_id}``, or of
    ``GET /agents-mgmt/agent/{agent_id}``.  The callback URIs, ``network``,
    ``subnet`` and ``creatorUserId`` are dropped.  ``scope`` is the account that
    listed the agent (None for the root account); ``organization_id`` is the
    organization it was listed under, or None when it came from ``get_agent``.
    """

    model_config = ConfigDict(populate_by_name=True)

    agent_id: str = Field(alias="agentId")
    name: str | None = None
    status: str | None = None
    agent_type: str | None = Field(default=None, alias="agentType")
    provider: str | None = None
    region: str | None = None
    system_id: str | None = Field(default=None, alias="systemId")
    scope: str | None = None
    organization_id: str | None = None

    @classmethod
    def from_occm(
        cls,
        occm: get_list_connectors.Occm,
        *,
        scope: str | None,
        organization_id: str,
    ) -> ConsoleAgentInfo:
        """Build from one ``occms`` item of the list-connectors response.

        Args:
            occm: Generated model from agentsmgmt/get_list_connectors.
            scope: The account scope that listed it, or None for the root.
            organization_id: The organization it was listed under.

        Returns:
            The compact agent.  A missing agent status falls back to the Occm status.

        Raises:
            pydantic.ValidationError: If the item has no ``agent.agentId``.
        """
        data = occm.agent.model_dump() if occm.agent is not None else {}
        if data.get("status") is None:
            data["status"] = occm.status
        return cls.model_validate({**data, "scope": scope, "organization_id": organization_id})

    @classmethod
    def from_agent(
        cls,
        body: get_agent.ResponseBody,
        *,
        scope: str | None,
        organization_id: str | None = None,
    ) -> ConsoleAgentInfo:
        """Build from the response of ``get_agent``.

        Args:
            body: Generated model from agentsmgmt/get_agent.
            scope: The account scope that fetched it, or None for the root.
            organization_id: The organization it belongs to, when known.

        Returns:
            The compact agent.

        Raises:
            pydantic.ValidationError: If the response has no ``agent.agentId``.
        """
        data = body.agent.model_dump() if body.agent is not None else {}
        return cls.model_validate({**data, "scope": scope, "organization_id": organization_id})


class ConsoleWorkingEnvironment(BaseModel):
    """Compact view of a Console working environment found by discovery (#1078).

    Source schema: an organization resource of type ``ON_PREM`` in the response of
    ``GET /v1/management/organizations/{organization_id}/resources``.
    ``public_id`` is the resource's ``rawId``, the id the Console agent uses for
    the working environment.  Mapping a working environment to its agents is not
    done here (#1076).
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str | None = None
    public_id: str | None = Field(default=None, alias="rawId")
    resource_type: str | None = Field(default=None, alias="resourceType")
    state: str | None = None
    scope: str | None = None
    organization_id: str

    @classmethod
    def from_resource(
        cls,
        resource: get_organizations_resources.Resource10GetResponseBody,
        *,
        scope: str | None,
        organization_id: str,
    ) -> ConsoleWorkingEnvironment:
        """Build from one organization resource.

        Args:
            resource: Generated model from tenancyv4/get_organizations_resources.
            scope: The account scope that listed it, or None for the root.
            organization_id: The organization it was listed under.

        Returns:
            The compact working environment.

        Raises:
            pydantic.ValidationError: If the resource has no ``id``.
        """
        data = resource.model_dump(include={"id", "name", "rawId", "resourceType", "state"})
        return cls.model_validate({**data, "scope": scope, "organization_id": organization_id})


__all__ = [
    "AccountSubscription",
    "Connector",
    "ConnectorSiteIdentifier",
    "ConsoleAgentInfo",
    "ConsoleWorkingEnvironment",
    "Folder",
    "MarketplaceSubscription",
    "Organization",
    "Project",
    "SubscriptionEntitlement",
]
