"""Generate client lock reports."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import click

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.options import filter_option
from pynetappfoundry.cli.utils import print_debug, print_error, print_info, print_success
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.models import ClusterConfig
from pynetappfoundry.models.ontap.protocols.locks import OntapClientLock
from pynetappfoundry.query import QuerySet
from pynetappfoundry.utils.excel import ExcelWorkbook


@click.command()
@filter_option()
@with_config("Locks report failed")
def locks(
    config: Config,
    clusters: dict[str, dict[str, Any]],
) -> None:
    """Generate client lock reports.

    Creates an Excel workbook with all client locks across
    matching clusters.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = config.output_dir / f"locks_{timestamp}.xlsx"
    wb = ExcelWorkbook(filename)

    failed: list[str] = []
    for name, details in clusters.items():
        print_info(f"Gathering lock data for {name}...")
        if not _gather_lock_data(name, details, config, wb):
            failed.append(name)

    wb.close()
    print_success(f"Report saved to {filename}")

    if clusters and len(failed) == len(clusters):
        raise click.ClickException(
            f"Could not gather lock data on any cluster: {', '.join(failed)}"
        )


def _gather_lock_data(
    name: str,
    details: dict[str, Any],
    config: Config,
    wb: ExcelWorkbook,
) -> bool:
    """Gather lock data from a single cluster.

    Returns:
        True on success, False if the cluster could not be queried.
    """
    try:
        cluster_config = ClusterConfig(**details)
        client = ONTAPAPIClient(cluster=cluster_config, config=config)

        locks_data: list[OntapClientLock] = QuerySet(OntapClientLock, client, config=config).all()

        ws = wb.add_sheet(name)
        ws.append(["Volume", "Protocol", "Type", "Path", "Lock", "State", "IP Address"])

        print_debug(f"Locks found: {len(locks_data)}")

        for lock in locks_data:
            try:
                lock_type = lock.type_
                if lock_type == "share_level":
                    ws.append(
                        [
                            lock.volume.name or "Unknown",
                            lock.protocol or "Unknown",
                            lock_type,
                            lock.path or "Unknown",
                            lock.share_lock.mode,
                            lock.state or "Unknown",
                            lock.client_address or "Unknown",
                        ]
                    )
                elif lock_type == "op_lock":
                    ws.append(
                        [
                            lock.volume.name or "Unknown",
                            lock.protocol or "Unknown",
                            lock_type,
                            lock.path or "Unknown",
                            lock.oplock_level,
                            lock.state or "Unknown",
                            lock.client_address or "Unknown",
                        ]
                    )
                else:
                    print_debug(f"Unknown lock type: {lock_type}")
            except Exception as e:
                print_error(f"Lock error: {e}")
        return True

    except Exception as e:
        print_error(f"Could not gather lock data for {name}: {e}")
        ws = wb.add_sheet(name)
        ws.append(["Error", str(e)])
        return False
