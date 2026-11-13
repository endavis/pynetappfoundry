"""Console agent (occm) API client, one instance per Console agent (ADR-0019)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from pydantic import SecretStr, ValidationError

from pynetappfoundry.clients.console.api import call_with_token
from pynetappfoundry.clients.console.auth import (
    ClientCredentialsTokenProvider,
    RefreshTokenProvider,
    TokenProvider,
)
from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.core.models import RetryConfig
from pynetappfoundry.models.console_types import Connector

if TYPE_CHECKING:
    import requests

    from pynetappfoundry.core.config import Config
    from pynetappfoundry.models.console.cvo import (
        get_occm_system_about,
        get_onprem_working_environments,
        get_onprem_working_environments_,
        post_onprem_working_environments,
    )

AGENT_ID_HEADER = "x-agent-id"

_LIST_PATH = "/occm/api/onprem/working-environments"
_ITEM_PATH = "/occm/api/onprem/working-environments/{workingEnvironmentId}"
_ABOUT_PATH = "/occm/api/occm/system/about"


def _join_fields(fields: str | Sequence[str] | None) -> str | None:
    """Return ``fields`` as the comma-joined string the agent expects."""
    if fields is None or isinstance(fields, str):
        return fields
    return ",".join(fields)


class ConsoleAgentClient:
    """Client for one Console agent's ``/occm/api``, reached through the Console SaaS host.

    Every request carries ``x-agent-id: <agent_id>`` (in the static ``auth_header``)
    and a bearer token.  Token source, first match wins: an injected
    ``token_provider``, a refresh token (user token via the refresh-token grant),
    ``user_token``, OAuth client credentials, ``service_token``.
    Static tokens go in ``auth_header``; provider tokens are sent per call with one
    refresh-and-retry on a 401.  ``add`` and ``delete`` are never retried on 5xx or
    timeouts.
    """

    def __init__(
        self,
        config: Config,
        agent_id: str,
        *,
        token_provider: TokenProvider | None = None,
        token_session: requests.Session | None = None,
    ) -> None:
        """Initialize the client.

        Args:
            config: Configuration object with Console API settings.
            agent_id: The Console agent id (non-empty).
            token_provider: Optional provider whose tokens are sent per call,
                for example ``ConsoleAPIClient.service_token_provider``.
            token_session: Optional ``requests.Session`` for the token exchange.

        Raises:
            ValueError: If ``agent_id`` is empty or blank.
            ConsoleAuthError: If client credentials are used and the initial
                token exchange fails.
        """
        if not isinstance(agent_id, str) or not agent_id.strip():
            raise ValueError("agent_id must be a non-empty string")
        self.config = config
        self.agent_id = agent_id
        settings = config.get_console_api_settings()
        spec_path = str(config.get_schema_location("console") / "console_openapi.yaml")

        auth_header: dict[str, str] = {AGENT_ID_HEADER: agent_id}
        self._provider: TokenProvider | None = None
        if token_provider is not None:
            self._provider = token_provider
        elif settings.refresh_token is not None:
            self._provider = RefreshTokenProvider(
                refresh_token=settings.refresh_token,
                client_id=settings.user_client_id,
                token_endpoint=settings.token_endpoint,
                timeout=settings.timeout,
                session=token_session,
            )
            # Fail fast on a bad refresh token rather than on the first API call.
            self._provider.get_token()
        elif settings.user_token:
            auth_header["Authorization"] = f"Bearer {settings.user_token}"
        elif settings.client_id and settings.client_secret:
            self._provider = ClientCredentialsTokenProvider(
                client_id=settings.client_id,
                client_secret=settings.client_secret,
                token_endpoint=settings.token_endpoint,
                audience=settings.audience,
                timeout=settings.timeout,
                session=token_session,
            )
            # Fail fast on bad credentials rather than on the first API call.
            self._provider.get_token()
        elif settings.service_token:
            auth_header["Authorization"] = f"Bearer {settings.service_token}"

        self._wrapper = APIWrapper(
            api_json_file=spec_path,
            base_url=settings.base_url,
            auth_header=auth_header,
            base_api_path=settings.base_api_path,
            timeout=settings.timeout,
            name="console-agent",
            use_operation_servers=True,
        )

    def _call(self, **kwargs: Any) -> Any:
        """Call an endpoint through the wrapper with token handling."""
        return call_with_token(self._wrapper, self._provider, **kwargs)

    def about(self) -> get_occm_system_about.ResponseBody:
        """GET /occm/api/occm/system/about.

        Returns:
            The agent's about information (includes ``agentId``).
        """
        from pynetappfoundry.models.console.cvo import get_occm_system_about as models

        response = self._call(method="GET", path_template=_ABOUT_PATH)
        if not isinstance(response, dict):
            raise TypeError(f"Expected a JSON object from about, got {type(response).__name__}")
        return models.ResponseBody.model_validate(response)

    def get_connector(self) -> Connector:
        """Return this agent as a compact ``Connector`` (from ``about()``).

        Returns:
            The Connector; ``agent_id`` falls back to this client's agent id.
        """
        return Connector.from_about(self.about(), agent_id=self.agent_id)

    def find_onprem_working_environment(
        self, cluster_uuid: str
    ) -> get_onprem_working_environments.ResponseBody | None:
        """Find the on-prem working environment of a cluster on this agent.

        Lists with ``fields=ontapClusterProperties`` and matches ``clusterUuid``.

        Args:
            cluster_uuid: The ONTAP cluster UUID.

        Returns:
            The matching working environment, or ``None`` when this agent has none.

        Raises:
            ValueError: If ``cluster_uuid`` is empty or blank.
        """
        if not isinstance(cluster_uuid, str) or not cluster_uuid.strip():
            raise ValueError("cluster_uuid must be a non-empty string")
        for item in self.list_onprem_working_environments(fields=["ontapClusterProperties"]):
            props = item.ontapClusterProperties
            if props is not None and props.clusterUuid == cluster_uuid:
                return item
        return None

    def list_onprem_working_environments(
        self,
        *,
        fields: str | Sequence[str] | None = None,
        tenant_id: str | None = None,
    ) -> list[get_onprem_working_environments.ResponseBody]:
        """GET /occm/api/onprem/working-environments.

        Args:
            fields: Extra fields to return (a string, or a sequence comma-joined).
            tenant_id: Optional tenant id filter (sent as ``tenantId``).

        Returns:
            The on-prem working environments.

        Raises:
            TypeError: If the response is not a JSON array.
        """
        from pynetappfoundry.models.console.cvo import get_onprem_working_environments as models

        query: dict[str, Any] = {}
        joined = _join_fields(fields)
        if joined is not None:
            query["fields"] = joined
        if tenant_id is not None:
            query["tenantId"] = tenant_id
        response = self._call(method="GET", path_template=_LIST_PATH, query_params=query or None)
        if not isinstance(response, list):
            raise TypeError(
                f"Expected a JSON array from the working environment list, "
                f"got {type(response).__name__}"
            )
        return [models.ResponseBody.model_validate(item) for item in response]

    def get_onprem_working_environment(
        self,
        working_environment_id: str,
        *,
        fields: str | Sequence[str] | None = None,
    ) -> get_onprem_working_environments_.ResponseBody:
        """GET /occm/api/onprem/working-environments/{workingEnvironmentId}.

        Args:
            working_environment_id: The working environment public id.
            fields: Extra fields to return (a string, or a sequence comma-joined).

        Returns:
            The working environment.
        """
        from pynetappfoundry.models.console.cvo import get_onprem_working_environments_ as models

        joined = _join_fields(fields)
        response = self._call(
            method="GET",
            path_template=_ITEM_PATH,
            path_params={"workingEnvironmentId": quote(working_environment_id, safe="")},
            query_params={"fields": joined} if joined is not None else None,
        )
        if not isinstance(response, dict):
            raise TypeError(
                f"Expected a JSON object from the working environment, "
                f"got {type(response).__name__}"
            )
        return models.ResponseBody.model_validate(response)

    def add_onprem_working_environment(
        self,
        *,
        tenant_id: str,
        cluster_address: str,
        cluster_user_name: str,
        cluster_password: SecretStr | str,
        name: str | None = None,
        description: str | None = None,
        location: str = "ON_PREM",
    ) -> post_onprem_working_environments.ResponseBody:
        """POST /occm/api/onprem/working-environments (never retried on 5xx or timeout).

        Args:
            tenant_id: The Console workspace id (``workspacePublicId``), not the
                ``Tenant-…`` value a working environment reports as ``tenantId``.
                The agent answers that value with HTTP 500.
            cluster_address: Cluster management address.
            cluster_user_name: Cluster user name.
            cluster_password: Cluster password; unwrapped only to build the body.
            name: Optional working environment name.
            description: Optional description.
            location: Location, ``ON_PREM`` by default.

        Returns:
            The created working environment.

        Raises:
            ValueError: If the inputs are invalid (the message names fields only).
            TypeError: If the response is not a JSON object.
        """
        from pynetappfoundry.models.console.cvo import post_onprem_working_environments as models

        password = (
            cluster_password.get_secret_value()
            if isinstance(cluster_password, SecretStr)
            else cluster_password
        )
        try:
            body = models.RequestBody(
                tenantId=tenant_id,
                clusterAddress=cluster_address,
                clusterUserName=cluster_user_name,
                clusterPassword=password,
                name=name,
                description=description,
                location=location,
            ).model_dump(exclude_none=True)
        except ValidationError as e:
            fields = ", ".join(".".join(str(p) for p in err["loc"]) for err in e.errors())
            # from None: the pydantic error would echo the password input.
            raise ValueError(f"Invalid working environment request: {fields}") from None
        response = self._call(
            method="POST",
            path_template=_LIST_PATH,
            body=body,
            retry_config=RetryConfig(enabled=False),
        )
        if not isinstance(response, dict):
            raise TypeError(
                f"Expected a JSON object from the working environment create, "
                f"got {type(response).__name__}"
            )
        return models.ResponseBody.model_validate(response)

    def delete_onprem_working_environment(self, working_environment_id: str) -> None:
        """DELETE /occm/api/onprem/working-environments/{workingEnvironmentId}.

        Never retried on 5xx or timeout.

        Args:
            working_environment_id: The working environment public id.
        """
        self._call(
            method="DELETE",
            path_template=_ITEM_PATH,
            path_params={"workingEnvironmentId": quote(working_environment_id, safe="")},
            retry_config=RetryConfig(enabled=False),
        )


__all__ = ["AGENT_ID_HEADER", "ConsoleAgentClient"]
