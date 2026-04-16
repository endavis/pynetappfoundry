# ruff: noqa: N815
"""DiiAuOnetimetoken information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAuOnetimetokenCommand(OntapModel):
    """DiiAuOnetimetokenCommand sub-model for commands."""

    commandTitle: str = ""
    command: str = ""


class DiiAuOnetimetoken(OntapModel):
    """DiiAuOnetimetoken information."""

    download: str = ""
    heading: str = ""
    footer: str = ""
    downloadTitle: str = ""
    name: str = ""
    description: str = ""
    commands: list[DiiAuOnetimetokenCommand] = Field(default_factory=list)
