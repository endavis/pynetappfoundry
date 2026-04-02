"""OntapDuo information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapDuoOwner(OntapModel):
    """OntapDuoOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


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
    owner: OntapDuoOwner = Field(default_factory=OntapDuoOwner)
    push_info: bool = False
    secret_key: str = ""
    status: str = ""
