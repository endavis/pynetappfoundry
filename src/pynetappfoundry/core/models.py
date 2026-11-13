"""Pydantic models for type-safe configuration."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator


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
    # Optional TLS CA validation for the ONTAP REST client (overrides global)
    verify_ssl: bool | None = None
    ca_bundle: str | None = None


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
    verify_ssl: bool = False
    ca_bundle: str | None = None


class DIIAPISettings(BaseModel):
    """Data Infrastructure Insights API settings."""

    model_config = ConfigDict(extra="allow")

    api_ro_token: str
    base_url: str
    base_api_path: str = "/rest/v1"
    timeout: float = 30.0


class ConsoleAPISettings(BaseModel):
    """Console SaaS API settings.

    At least one credential source is required: ``user_token`` (a user JWT from
    the BlueXP UI), ``service_token`` (a static service token), or OAuth client
    credentials (``client_id`` + ``client_secret``), which back the service slot
    with a token the client fetches and renews itself.  ``service_token`` and
    client credentials are mutually exclusive.  ``token_endpoint`` and
    ``audience`` only apply to client credentials.
    """

    # hide_input_in_errors keeps raw input values (including the client secret)
    # out of ValidationError text.
    model_config = ConfigDict(extra="allow", hide_input_in_errors=True)

    user_token: str | None = None
    service_token: str | None = None
    client_id: str | None = None
    client_secret: SecretStr | None = None
    token_endpoint: str = "https://netapp-cloud-account.auth0.com/oauth/token"
    audience: str = "https://api.cloud.netapp.com"
    base_url: str
    org_id: str | None = None
    base_api_path: str = "/"
    timeout: float = 30.0

    @property
    def uses_client_credentials(self) -> bool:
        """Whether the service slot is backed by an OAuth client-credentials grant."""
        return self.client_id is not None and self.client_secret is not None

    @model_validator(mode="after")
    def _validate_credential_sources(self) -> ConsoleAPISettings:
        """Validate the combination of credential fields (names only, never values)."""
        has_id = self.client_id is not None
        has_secret = self.client_secret is not None
        if has_id != has_secret:
            raise ValueError("client_id and client_secret must be set together")
        if has_id and self.service_token:
            raise ValueError(
                "service_token and client credentials (client_id/client_secret) "
                "are mutually exclusive; set only one"
            )
        if not has_id and ({"audience", "token_endpoint"} & self.model_fields_set):
            raise ValueError("audience and token_endpoint require client_id and client_secret")
        if not (self.user_token or self.service_token or has_id):
            raise ValueError(
                "one of user_token, service_token or client_id/client_secret is required"
            )
        return self


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


class PaginationConfig(BaseModel):
    """Configuration for API response pagination.

    Attributes:
        enabled: Whether pagination is enabled. Default True.
        max_pages: Maximum number of pages to fetch (1-10000). Default 100.
        records_key: Key in response dict containing the records list. Default "records".
        max_records: Stop following next links once this many records are
            collected, and truncate the result to it. ``None`` (default)
            fetches every page up to ``max_pages``.
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = True
    max_pages: int = Field(default=100, ge=1, le=10000)
    records_key: str = "records"
    max_records: int | None = Field(default=None, ge=1)


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
