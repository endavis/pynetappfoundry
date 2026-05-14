"""NetApp Foundry - ONTAP administration library and CLI tools."""

# Apply third-party perf patches before importing any Pydantic models so the
# patches are in place during every model_validate call. See _perf_patches.py
# for details. Tracked in issue #728.
import pynetappfoundry._perf_patches  # noqa: F401
from pynetappfoundry._version import __version__
from pynetappfoundry.clients.dii.api import DIIAPIClient
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.clients.ontap.cli import ONTAPCLI, CLICommandError
from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.logging import setup_logger
from pynetappfoundry.db.azevents import AzEventsDB
from pynetappfoundry.db.ems import EmsEventsDB
from pynetappfoundry.db.metrics import MetricDB

__all__ = [
    "ONTAPCLI",
    "APIWrapper",
    "AzEventsDB",
    "CLICommandError",
    "Config",
    "ConfigurationError",
    "DIIAPIClient",
    "EmsEventsDB",
    "MetricDB",
    "ONTAPAPIClient",
    "__version__",
    "setup_logger",
]
