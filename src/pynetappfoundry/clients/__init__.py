"""API client modules for ONTAP and Data Infrastructure Insights."""

from pynetappfoundry.clients.dii.api import DIIAPIClient
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.clients.ontap.cli import ONTAPCLI, CLICommandError, CLITimeoutError
from pynetappfoundry.clients.openapi import APIWrapper, NextPageExtractor, ontap_next_page_extractor

__all__ = [
    "ONTAPCLI",
    "APIWrapper",
    "CLICommandError",
    "CLITimeoutError",
    "DIIAPIClient",
    "NextPageExtractor",
    "ONTAPAPIClient",
    "ontap_next_page_extractor",
]
