"""Data Infrastructure Insights (DII) API client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pynetappfoundry.clients.openapi import APIWrapper

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config


class DIIAPIClient(APIWrapper):
    """API client for Data Infrastructure Insights (formerly Cloud Insights)."""

    def __init__(self, config: Config, **kwargs: Any) -> None:
        """Initialize the DII API client.

        Args:
            config: Configuration object with DII API settings.
            **kwargs: Additional arguments passed to APIWrapper.
        """
        self.config = config

        super().__init__(
            api_json_file=str(config.get_schema_location("dii") / "all.json"),
            base_url=config.settings["diiapi"]["general"]["base_url"],
            auth_header={
                "X-CloudInsights-ApiKey": self.config.settings["diiapi"]["general"][
                    "api_ro_token"
                ]
            },
            base_api_path=self.config.settings["diiapi"]["general"]["base_api_path"],
            **kwargs,
        )
