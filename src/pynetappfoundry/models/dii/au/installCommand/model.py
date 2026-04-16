# ruff: noqa: N815
"""DiiAuInstallcommand information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAuInstallcommandCommand(OntapModel):
    """DiiAuInstallcommandCommand sub-model for commands."""

    commandTitle: str = ""
    command: str = ""


class DiiAuInstallcommand(OntapModel):
    """DiiAuInstallcommand information."""

    download: str = ""
    heading: str = ""
    footer: str = ""
    downloadTitle: str = ""
    name: str = ""
    description: str = ""
    commands: list[DiiAuInstallcommandCommand] = Field(default_factory=list)
