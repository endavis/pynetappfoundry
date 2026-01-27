"""Pydantic models for type-safe configuration."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class BaseResource(BaseModel):
    """Base model for searchable resources.

    All fields are optional with empty string defaults to allow partial
    configuration. The 'name' field is typically set from the TOML key
    after parsing.
    """

    model_config = ConfigDict(extra="allow")

    name: str = ""
    ip: str = ""
    div: str = ""
    bu: str = ""
    env: str = ""


class ClusterConfig(BaseResource):
    """Configuration for an ONTAP cluster."""

    app: str = ""
    subapp: str = ""
    tags: list[str] = Field(default_factory=list)
    region: str = ""
    cloud: str = ""
    # Optional per-cluster credentials (override global)
    user: str | None = None
    enc: str | None = None


class AIQUMConfig(BaseResource):
    """Configuration for an Active IQ Unified Manager instance."""

    pass


class ConnectorConfig(BaseResource):
    """Configuration for a Cloud Insights connector."""

    pass


class CloudInsightsConfig(BaseResource):
    """Configuration for a Cloud Insights tenant."""

    pass


class AzureConfig(BaseResource):
    """Configuration for Azure resources."""

    subscription_id: str = ""
    resource_group: str = ""


class UserCredentials(BaseModel):
    """Credentials for a resource type."""

    model_config = ConfigDict(extra="allow")

    user: str
    enc: str


class SMTPSettings(BaseModel):
    """SMTP server configuration."""

    model_config = ConfigDict(extra="allow")

    server: str
    user: str = ""
    password: str = ""
    auth: str = "False"
    port: int = 25


class LicensingSettings(BaseModel):
    """Licensing notification settings."""

    model_config = ConfigDict(extra="allow")

    mailfrom: str
    mailto: str


class ONTAPAPISettings(BaseModel):
    """ONTAP REST API settings."""

    model_config = ConfigDict(extra="allow")

    base_api_path: str = "/api"


class DIIAPISettings(BaseModel):
    """Data Infrastructure Insights API settings."""

    model_config = ConfigDict(extra="allow")

    api_ro_token: str
    base_url: str
    base_api_path: str = "/rest/v1"


class SearchableKeysConfig(BaseModel):
    """Searchable keys configuration for a resource type."""

    model_config = ConfigDict(extra="allow")

    searchable_keys: list[str] = Field(default_factory=list)


# Type aliases for collections
ClusterCollection = dict[str, ClusterConfig]
AIQUMCollection = dict[str, AIQUMConfig]
ConnectorCollection = dict[str, ConnectorConfig]
CloudInsightsCollection = dict[str, CloudInsightsConfig]
AzureCollection = dict[str, AzureConfig]
