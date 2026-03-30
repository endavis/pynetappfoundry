"""OntapDuo information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapDuo(OntapModel):
    """OntapDuo information."""

    api_host: str = ""
    auto_push: bool = False
    comment: str = ""
    fail_mode: str = ""
    fingerprint: str = ""
    http_proxy: str = ""
    integration_key: str = ""
    is_enabled: bool = False
    max_prompts: int = 0
    owner_name: str = ""
    owner_uuid: str = ""
    push_info: bool = False
    secret_key: str = ""
    status: str = ""
