"""API client modules for ONTAP, AIQUM and Data Infrastructure Insights."""

from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient
from pynetappfoundry.clients.console.agent import ConsoleAgentClient
from pynetappfoundry.clients.dii.api import DIIAPIClient
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.clients.ontap.cli import ONTAPCLI, CLICommandError, CLITimeoutError
from pynetappfoundry.clients.openapi import APIWrapper, NextPageExtractor, ontap_next_page_extractor

__all__ = [
    "ONTAPCLI",
    "AIQUMAPIClient",
    "APIWrapper",
    "CLICommandError",
    "CLITimeoutError",
    "ConsoleAgentClient",
    "DIIAPIClient",
    "NextPageExtractor",
    "ONTAPAPIClient",
    "ontap_next_page_extractor",
]
