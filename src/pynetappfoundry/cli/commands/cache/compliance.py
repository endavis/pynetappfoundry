"""Cache compliance command for running compliance checks against cached data.

Evaluates compliance rules defined in TOML configuration against cached
cluster metadata and reports violations.

Exit codes:
- 0: no violations found
- 1: violations found
- 2: error, including any compliance rule that was invalid or failed
  (reported on stderr with its reason; violations are still printed)
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path

import click
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from pynetappfoundry.cache import ClusterMetadataDB
from pynetappfoundry.cli.utils import print_error, print_warning
from pynetappfoundry.compliance.config import (
    get_cluster_overrides,
    load_global_compliance_rules,
    merge_rules,
)
from pynetappfoundry.compliance.engine import run_compliance_checks
from pynetappfoundry.compliance.models import ComplianceResult, ComplianceRuleError
from pynetappfoundry.core.config import Config

console = Console()
err_console = Console(stderr=True)

# Severity ordering for --severity filtering
_SEVERITY_LEVELS = {"info": 0, "warning": 1, "error": 2}


def _severity_at_least(result_severity: str, min_severity: str) -> bool:
    """Check if a result severity meets the minimum threshold.

    Args:
        result_severity: The severity of the result.
        min_severity: The minimum severity to include.

    Returns:
        True if the result severity is at or above the minimum.
    """
    result_level = _SEVERITY_LEVELS.get(result_severity, 0)
    min_level = _SEVERITY_LEVELS.get(min_severity, 0)
    return result_level >= min_level


def _report_rule_errors(errors: list[ComplianceRuleError]) -> None:
    """Print compliance rule errors to stderr, one line each.

    Args:
        errors: Rule errors to report.
    """
    for err in errors:
        where = f" (cluster {escape(err.cluster_name)})" if err.cluster_name else ""
        err_console.print(
            f"[red]Compliance rule '{escape(err.rule_name)}'{where} "
            f"{escape(f'[{err.stage}]')}: {escape(err.message)}[/red]",
            soft_wrap=True,
            markup=True,
            highlight=False,
        )


def _output_table(results: list[ComplianceResult]) -> Table:
    """Build a Rich Table from compliance results.

    Args:
        results: List of ComplianceResult instances.

    Returns:
        Rich Table instance.
    """
    table = Table(title="Compliance Check Results")
    table.add_column("Cluster", style="bold")
    table.add_column("Rule", style="cyan")
    table.add_column("Severity", style="magenta")
    table.add_column("Matches", style="red")
    table.add_column("Description")

    for result in results:
        table.add_row(
            escape(result.cluster_name),
            escape(result.rule_name),
            escape(result.severity),
            str(result.match_count),
            escape(result.description),
        )

    return table


def _output_json(results: list[ComplianceResult]) -> str:
    """Format results as JSON.

    Args:
        results: List of ComplianceResult instances.

    Returns:
        JSON string.
    """
    return json.dumps([r.model_dump() for r in results], default=str)


def _output_csv(results: list[ComplianceResult]) -> str:
    """Format results as CSV.

    Args:
        results: List of ComplianceResult instances.

    Returns:
        CSV string.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["cluster", "rule", "severity", "match_count", "description"])

    for result in results:
        writer.writerow(
            [
                result.cluster_name,
                result.rule_name,
                result.severity,
                result.match_count,
                result.description,
            ]
        )

    return output.getvalue().rstrip("\r\n")


@click.command()
@click.argument("cluster", required=False)
@click.option(
    "--all",
    "query_all",
    is_flag=True,
    help="Check all cached clusters.",
)
@click.option(
    "--filter",
    "-f",
    "filter_str",
    help='JSON filter for cluster selection: \'{"bu":"Business", "env":"Prod"}\'',
)
@click.option(
    "--check",
    "-k",
    "check_name",
    help="Run only the named compliance rule.",
)
@click.option(
    "--severity",
    "-s",
    "min_severity",
    type=click.Choice(["info", "warning", "error"], case_sensitive=False),
    help="Minimum severity to report.",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON.",
)
@click.option(
    "--csv",
    "output_csv",
    is_flag=True,
    help="Output as CSV with header row.",
)
@click.pass_context
def compliance(
    ctx: click.Context,
    cluster: str | None,
    query_all: bool,
    filter_str: str | None,
    check_name: str | None,
    min_severity: str | None,
    output_json: bool,
    output_csv: bool,
) -> None:
    """Run compliance checks against cached cluster metadata.

    Evaluates compliance rules from TOML configuration against cached data.
    Rules define a model and filter expression — any matching records are
    violations.

    Exit codes: 0 = no violations, 1 = violations found, 2 = error (including
    invalid or failing rules, reported on stderr).

    \b
    Examples:
        # Check a single cluster
        nf cache compliance cluster1

        # Check all cached clusters
        nf cache compliance --all

        # Filter clusters and run a specific check
        nf cache compliance -f '{"env":"Prod"}' -k vol_autosize

        # Only show errors
        nf cache compliance --all -s error

        # JSON output for scripting
        nf cache compliance --all --json
    """
    config_dir = ctx.obj.get("config_dir", "config")

    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(2)

    try:
        config = Config(config_dir=config_dir, script_name="cache-compliance")
    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        ctx.exit(2)

    # Load global compliance rules
    rule_errors: list[ComplianceRuleError] = []
    global_rules = load_global_compliance_rules(config, errors=rule_errors)
    if check_name is not None:
        rule_errors = [e for e in rule_errors if e.rule_name == check_name]
    _report_rule_errors(rule_errors)
    # Load errors are reported once; later errors are per cluster.
    exit_on_empty = 2 if rule_errors else 0
    if not global_rules:
        if not rule_errors:
            print_warning("No compliance rules defined in configuration.")
        ctx.exit(exit_on_empty)

    # Determine cluster list (same logic as check.py)
    cluster_names: list[str] = []
    db = ClusterMetadataDB(config=config)

    if cluster:
        cluster_names = [cluster]
    elif query_all:
        cached = db.list_clusters()
        cluster_names = [c["cluster_name"] for c in cached]
        if not cluster_names:
            print_warning("No cached clusters found. Use 'nf cache refresh' to populate.")
            db.close()
            ctx.exit(exit_on_empty)
    elif filter_str:
        try:
            filter_dict = json.loads(filter_str)
        except json.JSONDecodeError as e:
            print_error(f"Invalid filter JSON: {e}")
            db.close()
            ctx.exit(2)

        filtered = config.get_clusters(filter_dict)
        if not filtered:
            print_warning("No clusters match the filter criteria.")
            db.close()
            ctx.exit(exit_on_empty)
        cluster_names = list(filtered.keys())
    else:
        print_error("Must specify CLUSTER, --all, or --filter/-f")
        db.close()
        ctx.exit(2)

    # Run checks for each cluster
    all_results: list[ComplianceResult] = []

    for name in cluster_names:
        cluster_entry = config.data.get("clusters", {}).get(name)
        if cluster_entry is not None:
            cluster_errors: list[ComplianceRuleError] = []
            overrides = get_cluster_overrides(
                cluster_entry, errors=cluster_errors, cluster_name=name
            )
            effective_rules = merge_rules(
                global_rules, overrides, errors=cluster_errors, cluster_name=name
            )
            if check_name is not None:
                cluster_errors = [e for e in cluster_errors if e.rule_name == check_name]
            _report_rule_errors(cluster_errors)
            rule_errors.extend(cluster_errors)
        else:
            effective_rules = {k: v.model_copy() for k, v in global_rules.items()}

        query_errors: list[ComplianceRuleError] = []
        results = run_compliance_checks(
            db, name, effective_rules, check_filter=check_name, errors=query_errors
        )
        _report_rule_errors(query_errors)
        rule_errors.extend(query_errors)
        all_results.extend(results)

    db.close()

    # Filter by minimum severity
    if min_severity:
        all_results = [r for r in all_results if _severity_at_least(r.severity, min_severity)]

    # Output
    if not all_results:
        ctx.exit(2 if rule_errors else 0)

    if output_json:
        console.print(_output_json(all_results), soft_wrap=True)
    elif output_csv:
        console.print(_output_csv(all_results), soft_wrap=True)
    else:
        table = _output_table(all_results)
        console.print(table)

    # Violations are printed above; a rule error still takes precedence.
    ctx.exit(2 if rule_errors else 1)
