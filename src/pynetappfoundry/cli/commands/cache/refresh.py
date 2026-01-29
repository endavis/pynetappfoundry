"""Cache refresh command."""

from __future__ import annotations

import contextlib
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from pynetappfoundry.cache import ClusterMetadataDB, MetadataCollector
from pynetappfoundry.cli.utils import print_error, print_exception, print_success, print_warning
from pynetappfoundry.clients.ontap import ONTAPCLI, ONTAPAPIClient
from pynetappfoundry.core.config import Config

console = Console()


@click.command()
@click.argument("cluster", required=False)
@click.option(
    "--all",
    "-a",
    "refresh_all",
    is_flag=True,
    help="Refresh cache for all configured clusters.",
)
@click.pass_context
def refresh(ctx: click.Context, cluster: str | None, refresh_all: bool) -> None:
    """Refresh the metadata cache for cluster(s).

    If CLUSTER is specified, refresh only that cluster.
    Use --all to refresh all configured clusters.

    Examples:

        nf cache refresh cluster1      # Refresh single cluster
        nf cache refresh --all         # Refresh all clusters
    """
    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-refresh")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(1)

    # Determine clusters to refresh
    if cluster:
        if cluster not in config.data.get("clusters", {}):
            print_error(f"Cluster '{cluster}' not found in configuration.")
            available = list(config.data.get("clusters", {}).keys())
            if available:
                console.print(f"Available clusters: {', '.join(available)}")
            ctx.exit(1)
        clusters_to_refresh = [cluster]
    elif refresh_all:
        clusters_to_refresh = list(config.data.get("clusters", {}).keys())
        if not clusters_to_refresh:
            print_warning("No clusters configured.")
            ctx.exit(0)
    else:
        print_error("Specify a cluster name or use --all to refresh all clusters.")
        ctx.exit(1)

    # Initialize cache database
    db = ClusterMetadataDB(config=config)

    console.print(f"\nRefreshing cache for {len(clusters_to_refresh)} cluster(s)...\n")

    success_count = 0
    error_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for cluster_name in clusters_to_refresh:
            task = progress.add_task(f"Collecting metadata for {cluster_name}...", total=1)

            try:
                cluster_data = config.data["clusters"][cluster_name]

                # Get credentials
                user, password = config.get_user("clusters", cluster_name)

                # Create cluster object for API client
                class ClusterObj:
                    def __init__(self, name: str, ip: str) -> None:
                        self.name = name
                        self.ip = ip

                cluster_obj = ClusterObj(cluster_name, cluster_data.get("ip", ""))

                # Initialize clients
                api_client: ONTAPAPIClient | None = None
                cli_client: ONTAPCLI | None = None

                try:
                    api_client = ONTAPAPIClient(cluster=cluster_obj, config=config)
                except Exception as e:
                    print_warning(f"  API client unavailable: {e}")

                try:
                    cli_client = ONTAPCLI(
                        name=cluster_name,
                        host_or_ip=cluster_data.get("ip", ""),
                        username=user,
                        password=password,
                    )
                except Exception as e:
                    print_warning(f"  CLI client unavailable: {e}")

                if not api_client and not cli_client:
                    print_error(f"  No clients available for {cluster_name}")
                    error_count += 1
                    progress.update(task, completed=1)
                    continue

                # Collect metadata
                collector = MetadataCollector(api_client=api_client, cli_client=cli_client)
                metadata = collector.collect_all(cluster_name)

                # Store in cache
                db.set(cluster_name, metadata)

                # Clean up CLI client
                if cli_client:
                    with contextlib.suppress(Exception):
                        cli_client.disconnect()

                print_success(f"  {cluster_name}: Cache refreshed")
                success_count += 1

            except Exception as e:
                print_exception(f"  {cluster_name}: Failed - {e}", e)
                error_count += 1

            progress.update(task, completed=1)

    db.close()

    # Summary
    console.print()
    if success_count > 0:
        print_success(f"Successfully refreshed {success_count} cluster(s)")
    if error_count > 0:
        print_error(f"Failed to refresh {error_count} cluster(s)")
        ctx.exit(1)
