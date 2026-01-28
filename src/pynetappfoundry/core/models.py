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
    timeout: float = 30.0


class DIIAPISettings(BaseModel):
    """Data Infrastructure Insights API settings."""

    model_config = ConfigDict(extra="allow")

    api_ro_token: str
    base_url: str
    base_api_path: str = "/rest/v1"
    timeout: float = 30.0


class SearchableKeysConfig(BaseModel):
    """Searchable keys configuration for a resource type."""

    model_config = ConfigDict(extra="allow")

    searchable_keys: list[str] = Field(default_factory=list)


class RetryConfig(BaseModel):
    """Configuration for HTTP retry behavior.

    Attributes:
        enabled: Whether retry is enabled. Default True.
        max_attempts: Maximum number of retry attempts (1-10). Default 3.
        initial_wait: Initial wait time in seconds before first retry. Default 1.0.
        max_wait: Maximum wait time in seconds between retries. Default 60.0.
        exponential_base: Base for exponential backoff calculation. Default 2.
        retryable_status_codes: HTTP status codes that trigger a retry.
        retry_on_connection_error: Whether to retry on connection errors. Default True.
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = True
    max_attempts: int = Field(default=3, ge=1, le=10)
    initial_wait: float = Field(default=1.0, ge=0.1)
    max_wait: float = Field(default=60.0, ge=1.0)
    exponential_base: int = Field(default=2, ge=2)
    retryable_status_codes: list[int] = Field(default_factory=lambda: [429, 500, 502, 503, 504])
    retry_on_connection_error: bool = True


class ValidationConfig(BaseModel):
    """Configuration for response validation behavior.

    Attributes:
        enabled: Whether validation is enabled. Default False (opt-in).
        strict: If True, raise exception on validation failure. If False, log warning.
        validate_success_only: Only validate 2xx responses. Default True.
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = False
    strict: bool = False
    validate_success_only: bool = True


class CacheConfig(BaseModel):
    """Configuration for cluster metadata caching.

    Attributes:
        cache_dir: Override cache directory location. If empty, uses default
                   ({config_dir}/.cache).
        cache_ttl_days: Number of days before cache is considered stale.
                        Used for warnings, not automatic refresh.
        auto_warn_stale: Warn when cached data is stale. Default True.
        auto_warn_empty: Warn when cache is empty for a cluster. Default True.
    """

    model_config = ConfigDict(extra="forbid")

    cache_dir: str = ""
    cache_ttl_days: int = Field(default=30, ge=1)
    auto_warn_stale: bool = True
    auto_warn_empty: bool = True


# Type aliases for collections
ClusterCollection = dict[str, ClusterConfig]
AIQUMCollection = dict[str, AIQUMConfig]
ConnectorCollection = dict[str, ConnectorConfig]
CloudInsightsCollection = dict[str, CloudInsightsConfig]
AzureCollection = dict[str, AzureConfig]
