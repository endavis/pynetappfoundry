"""API client modules for ONTAP, AIQUM, Data Infrastructure Insights and Digital Advisor."""

from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient
from pynetappfoundry.clients.console.agent import ConsoleAgentClient
from pynetappfoundry.clients.digitaladvisor.api import DigitalAdvisorAPIClient
from pynetappfoundry.clients.dii.api import DIIAPIClient, DIIWriteTokenMissingError
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
    "DIIWriteTokenMissingError",
    "DigitalAdvisorAPIClient",
    "NextPageExtractor",
    "ONTAPAPIClient",
    "ontap_next_page_extractor",
]
