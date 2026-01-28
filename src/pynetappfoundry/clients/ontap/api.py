"""ONTAP API client."""

from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Any

import urllib3

from pynetappfoundry.clients.openapi import APIWrapper

# Suppress InsecureRequestWarning since we intentionally disable SSL verification
# for ONTAP clusters with self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config


class ONTAPAPIClient(APIWrapper):
    """API client for ONTAP clusters using OpenAPI specification."""

    def __init__(
        self,
        cluster: Any,
        config: Config,
        **kwargs: Any,
    ) -> None:
        """Initialize the ONTAP API client.

        Args:
            cluster: Cluster object with 'name' and 'ip' attributes.
            config: Configuration object.
            **kwargs: Additional arguments passed to APIWrapper.
        """
        self.cluster = cluster
        self.config = config

        user, enc = self.config.get_user("clusters", cluster.name)
        b64string = base64.b64encode(f"{user}:{enc}".encode("ascii"))
        auth_header = {"authorization": f"Basic {b64string.decode()}"}

        ontap_settings = config.get_ontap_api_settings()
        super().__init__(
            api_json_file=str(config.get_schema_location("ontap") / "all.json"),
            base_url=f"https://{cluster.ip}",
            auth_header=auth_header,
            base_api_path=ontap_settings.base_api_path,
            timeout=ontap_settings.timeout,
            verify_ssl=False,  # ONTAP clusters typically use self-signed certs
            **kwargs,
        )
