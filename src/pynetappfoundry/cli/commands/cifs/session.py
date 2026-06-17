"""Inspect active CIFS/SMB sessions across in-scope clusters.

Implements ``nf cifs session`` per issue #775. All ONTAP reads go through
:class:`~pynetappfoundry.data.source.DataSource` (ADR-0012/0013); no
direct ``HostConnection`` or ``netapp_ontap`` SDK use.
"""

from __future__ import annotations

import csv
import fnmatch
import ipaddress
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import click
from rich.table import Table

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import (
    console,
    print_exception,
    print_info,
    print_warning,
)
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.ontap.protocols.cifs.sessions.model import OntapCifsSession

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

# Column headers used for both Rich table and CSV output.
COLUMNS: tuple[str, ...] = (
    "Cluster",
    "SVM",
    "User",
    "Mapped Unix User",
    "Client IP",
    "Server IP",
    "Protocol",
    "Auth",
    "Encryption",
    "Connected",
    "Idle",
    "Open Files",
    "Open Shares",
)

# Glob metacharacters that flip ``--user`` from substring to glob match
# and disable server-side push.
_GLOB_CHARS = "*?["


SessionRow = tuple[str, ...]


def _has_glob(value: str) -> bool:
    """Return True if *value* contains glob metacharacters."""
    return any(ch in value for ch in _GLOB_CHARS)


def _matches_user(
    session_user: str,
    mapped_unix_user: str,
    pattern: str,
    case_sensitive: bool,
) -> bool:
    """Return True if *pattern* matches ``user`` or ``mapped_unix_user``.

    A pattern with no glob metacharacters is treated as a substring match.
    A pattern with metacharacters (``*``, ``?``, ``[``) is matched with
    :func:`fnmatch.fnmatchcase`.

    Empty patterns always return False; empty haystacks never match.
    """
    if not pattern:
        return False

    needle = pattern if case_sensitive else pattern.lower()
    is_glob = _has_glob(needle)

    for raw in (session_user, mapped_unix_user):
        if not raw:
            continue
        haystack = raw if case_sensitive else raw.lower()
        if is_glob:
            if fnmatch.fnmatchcase(haystack, needle):
                return True
        elif needle in haystack:
            return True
    return False


def _is_plain_ip(value: str) -> bool:
    """Return True if *value* parses as a single IPv4/IPv6 address."""
    try:
        ipaddress.ip_address(value)
    except ValueError:
        return False
    return True


def _is_cidr(value: str) -> bool:
    """Return True if *value* parses as an IPv4/IPv6 network."""
    if "/" not in value:
        return False
    try:
        ipaddress.ip_network(value, strict=False)
    except ValueError:
        return False
    return True


def _matches_ip(client_ip: str, pattern: str) -> bool:
    """Return True if *client_ip* matches the IP filter *pattern*.

    Supports:

    - Exact IP (``10.1.2.45``).
    - Glob (``10.1.2.*``) — matched with :func:`fnmatch.fnmatchcase`.
    - CIDR (``10.1.2.0/24``) — parsed with :mod:`ipaddress`.

    Empty *pattern* or *client_ip* returns False. Address-family
    mismatches between a v4 network and a v6 address (or vice-versa)
    return False, never raise.
    """
    if not pattern or not client_ip:
        return False

    if _is_cidr(pattern):
        try:
            net = ipaddress.ip_network(pattern, strict=False)
            addr = ipaddress.ip_address(client_ip)
        except ValueError:
            return False
        if net.version != addr.version:
            return False
        return addr in net

    if _has_glob(pattern):
        return fnmatch.fnmatchcase(client_ip, pattern)

    # Plain IP: compare as parsed addresses to normalize form, fall back
    # to string equality for non-parseable inputs (defensive).
    try:
        return ipaddress.ip_address(pattern) == ipaddress.ip_address(client_ip)
    except ValueError:
        return pattern == client_ip


def _validate_ip_pattern(pattern: str) -> None:
    """Raise :class:`click.BadParameter` if *pattern* is not a valid IP filter.

    Accepts plain IP, glob, or CIDR. An empty pattern is rejected — Click
    will not invoke this for unset options.
    """
    if not pattern:
        msg = "IP filter must not be empty."
        raise click.BadParameter(msg)
    if _is_cidr(pattern):
        try:
            ipaddress.ip_network(pattern, strict=False)
        except ValueError as e:
            raise click.BadParameter(f"Invalid CIDR: {pattern}") from e
        return
    if _has_glob(pattern):
        return
    if not _is_plain_ip(pattern):
        msg = f"Invalid IP, glob, or CIDR: {pattern!r}"
        raise click.BadParameter(msg)


def _row_for(cluster: str, session: OntapCifsSession) -> SessionRow:
    """Project an :class:`OntapCifsSession` to a display row."""
    return (
        cluster,
        session.svm.name,
        session.user,
        session.mapped_unix_user,
        session.client_ip,
        session.server_ip,
        session.protocol,
        session.authentication,
        session.smb_encryption,
        session.connected_duration,
        session.idle_duration,
        str(session.open_files),
        str(session.open_shares),
    )


def _scan_cluster(
    config: Config,
    cluster: str,
    user: str | None,
    case_sensitive: bool,
    ip: str | None,
) -> tuple[list[SessionRow], int]:
    """Scan a single cluster's CIFS sessions via :class:`DataSource`.

    Always runs in live mode (``source="live"``) because CIFS sessions
    are transient and not part of :class:`CachedClusterMetadata`.

    Server-side push:

    - ``--ip`` (plain IP) -> ``qb.filter({"client_ip": value})``.

    ``--user`` is not pushed server-side: ``_matches_user`` matches
    either ``user`` or ``mapped_unix_user``, and a server-side ``user=``
    filter would incorrectly drop sessions whose ``mapped_unix_user``
    matches but whose ``user`` does not. Glob, CIDR, and case-insensitive
    matches are handled client-side.

    Returns:
        ``(rows, scanned)`` for the cluster.
    """
    ds = DataSource(config)
    qb = ds.query(OntapCifsSession, cluster=cluster, source="live")

    # NOTE: ``user`` is not pushed server-side. ``_matches_user`` matches
    # either ``user`` OR ``mapped_unix_user``; a server-side ``user=``
    # filter would incorrectly drop sessions whose ``mapped_unix_user``
    # matches but whose ``user`` does not. ``client_ip`` is safe to push
    # because it is the only field we filter on for IP.
    if ip and _is_plain_ip(ip):
        qb = qb.filter({"client_ip": ip})

    rows: list[SessionRow] = []
    scanned = 0
    for session in qb:
        scanned += 1
        if user and not _matches_user(session.user, session.mapped_unix_user, user, case_sensitive):
            continue
        if ip and not _matches_ip(session.client_ip, ip):
            continue
        rows.append(_row_for(cluster, session))
    return rows, scanned


def _render_table(rows: list[SessionRow], title: str) -> None:
    """Render *rows* as a Rich table with no truncation or wrapping.

    Each column is configured with ``no_wrap=True, overflow="ignore"``
    so long values (DOMAIN\\user, durations, etc.) never get elided.
    The table is rendered through a private Console that wraps the
    module-level ``console.file`` at an effectively unbounded width so
    Rich does not collapse columns to fit a narrow terminal — long rows
    overflow horizontally instead. This matches the no-truncation
    contract in issue #775.
    """
    from rich.console import Console as _RichConsole

    table = Table(title=title, show_lines=False)
    for col in COLUMNS:
        table.add_column(col, no_wrap=True, overflow="ignore")
    for row in rows:
        table.add_row(*row)
    wide = _RichConsole(
        file=console.file,
        width=10_000,
        force_terminal=False,
        no_color=console.no_color,
        record=False,
    )
    wide.print(table)


def _resolve_csv_path(csv_arg: str, output_dir: str | Path) -> Path:
    """Return the CSV target path.

    If *csv_arg* points to an existing directory, write
    ``cifs_sessions_<YYYYMMDD-HHMMSS>.csv`` inside it. Otherwise treat
    *csv_arg* as the explicit target file. If the path ends with a
    separator and does not yet exist, treat it as a directory and
    create it.
    """
    path = Path(csv_arg)
    if path.is_dir() or csv_arg.endswith(("/", "\\")):
        path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(tz=UTC).strftime("%Y%m%d-%H%M%S")
        return path / f"cifs_sessions_{timestamp}.csv"
    if not csv_arg:  # pragma: no cover - Click prevents empty value
        timestamp = datetime.now(tz=UTC).strftime("%Y%m%d-%H%M%S")
        return Path(output_dir) / f"cifs_sessions_{timestamp}.csv"
    return path


def _write_csv(rows: list[SessionRow], path: Path) -> None:
    """Write *rows* to *path* as UTF-8 CSV with the standard header row."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(COLUMNS)
        writer.writerows(rows)


@click.command("session")
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON cluster filter: \'{"bu":"Business","env":"Prod"}\'.',
)
@click.option(
    "--user",
    "-u",
    "user",
    default=None,
    help=(
        "Match CIFS session ``user`` or ``mapped_unix_user``. Substring "
        "match unless glob metacharacters (``*``, ``?``, ``[``) are "
        "present, e.g. ``*jdoe*``, ``DOMAIN\\\\jdoe``."
    ),
)
@click.option(
    "--ip",
    "-i",
    "ip",
    default=None,
    help=(
        "Match ``client_ip``. Accepts an exact IP (``10.1.2.45``), glob "
        "(``10.1.2.*``), or CIDR (``10.1.2.0/24``)."
    ),
)
@click.option(
    "--case-sensitive/--case-insensitive",
    "case_sensitive",
    default=False,
    show_default=True,
    help="Match the ``--user`` pattern case-sensitively.",
)
@click.option(
    "--csv",
    "-c",
    "csv_path",
    type=click.Path(),
    default=None,
    help=(
        "Write results to a CSV file *in addition to* the Rich table. "
        "If PATH is a directory, writes "
        "``cifs_sessions_<YYYYMMDD-HHMMSS>.csv`` inside it."
    ),
)
@with_config("Get CIFS sessions failed")
def session(
    config: Config,
    clusters: dict[str, dict[str, Any]],
    user: str | None,
    ip: str | None,
    case_sensitive: bool,
    csv_path: str | None,
) -> None:
    """List active CIFS/SMB sessions across in-scope clusters.

    Examples:
        nf cifs session
        nf cifs session -u 'DOMAIN\\jdoe'
        nf cifs session -u '*jdoe*' -f '{"env":"Prod"}'
        nf cifs session -i 10.1.2.45
        nf cifs session -i 10.1.2.0/24
        nf cifs session -u jdoe -i 10.1.2.0/24 --case-sensitive
        nf cifs session -u jdoe --csv ./jdoe-sessions.csv

    CIFS sessions are transient and never cached; every invocation
    queries each in-scope cluster live via the ONTAP REST API.
    """
    if ip is not None:
        _validate_ip_pattern(ip)

    if not clusters:
        print_warning("No clusters matched the filter; nothing to scan.")
        return

    filter_desc: list[str] = []
    if user:
        mode = "case-sensitive" if case_sensitive else "case-insensitive"
        filter_desc.append(f"user={user!r} ({mode})")
    if ip:
        filter_desc.append(f"ip={ip!r}")
    desc = " and ".join(filter_desc) if filter_desc else "all sessions"
    print_info(f"Scanning {len(clusters)} cluster(s) for {desc}...")

    all_rows: list[SessionRow] = []
    for idx, (name, details) in enumerate(clusters.items(), start=1):
        print_info(
            f"[{idx}/{len(clusters)}] {name} ({details.get('ip', '?')}): querying CIFS sessions..."
        )
        try:
            rows, scanned = _scan_cluster(config, name, user, case_sensitive, ip)
        except Exception as e:
            print_exception(f"Could not query CIFS sessions on {name}: {e}", e)
            continue
        all_rows.extend(rows)
        print_info(
            f"[{idx}/{len(clusters)}] {name}: scanned {scanned} session(s), matched {len(rows)}."
        )

    title = f"CIFS Sessions ({desc})"
    if not all_rows:
        console.print(f"[yellow]No CIFS sessions matched ({desc}).[/yellow]")
    else:
        _render_table(all_rows, title)
        print_info(f"Total matching sessions: {len(all_rows)}")

    if csv_path is not None:
        target = _resolve_csv_path(csv_path, config.output_dir)
        _write_csv(all_rows, target)
        print_info(f"CSV written to {target.resolve()} ({len(all_rows)} row(s)).")
