"""CLI command groups."""

from pynetappfoundry.cli.commands.cifs import cifs
from pynetappfoundry.cli.commands.events import events
from pynetappfoundry.cli.commands.licenses import licenses
from pynetappfoundry.cli.commands.metrics import metrics
from pynetappfoundry.cli.commands.reports import reports
from pynetappfoundry.cli.commands.utils import utils

__all__ = ["cifs", "events", "licenses", "metrics", "reports", "utils"]
