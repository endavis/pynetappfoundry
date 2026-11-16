"""Active IQ Unified Manager (AIQUM) API client."""

from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Any

from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.clients.trust import FingerprintPinningAdapter
from pynetappfoundry.core.config import ConfigurationError
from pynetappfoundry.core.models import AIQUMConfig

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config


class AIQUMAPIClient(APIWrapper):
    """API client for an Active IQ Unified Manager instance.

    The target is ``config.data["aiqums"][name]`` and the credentials come from
    ``users.toml [aiqums]``. TLS is pinned on first use (chain validation is off).

    Paging needs no AIQUM-specific code: the inherited ``get_all_records``
    follows the HAL ``_links.next.href`` links and merges ``records``.

    POST is retried by default, so pass ``retry_config=RetryConfig(enabled=False)``
    for non-idempotent calls.
    """

    def __init__(self, name: str, config: Config, **kwargs: Any) -> None:
        """Initialize the AIQUM API client.

        Args:
            name: Key of the instance in the ``[aiqums]`` inventory.
            config: Configuration object.
            **kwargs: Additional arguments passed to APIWrapper.

        Raises:
            ConfigurationError: If the instance is unknown or has no ``ip``, or
                ``aiqumapi.toml`` has no ``[general]`` section.
        """
        entry = config.data.get("aiqums", {}).get(name)
        if not isinstance(entry, dict):
            raise ConfigurationError(f"No AIQUM named {name!r} in the [aiqums] inventory.")
        aiqum = AIQUMConfig.model_validate({**entry, "name": name})
        if not aiqum.ip:
            raise ConfigurationError(f"AIQUM {name!r} has no ip; set aiqums.{name}.ip.")

        settings = config.get_aiqum_api_settings()

        user, password = config.get_user("aiqums", name)
        b64string = base64.b64encode(f"{user}:{password}".encode("ascii"))
        auth_header = {"authorization": f"Basic {b64string.decode()}"}

        self.aiqum = aiqum
        self.config = config
        super().__init__(
            api_json_file=str(config.get_schema_location("aiqum") / "all.json"),
            base_url=f"https://{aiqum.ip}",
            auth_header=auth_header,
            base_api_path=settings.base_api_path,
            timeout=settings.timeout,
            # Pin only: chain validation off, the fingerprint is pinned instead.
            verify_ssl=False,
            https_adapter=FingerprintPinningAdapter(
                config.get_trust_store().tls, pool_connections=20, pool_maxsize=20
            ),
            name=name,
            **kwargs,
        )
