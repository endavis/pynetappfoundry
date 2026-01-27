"""Convert SQLite database to Excel."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import click
from openpyxl import Workbook

from pynetappfoundry.cli.utils import print_error, print_info, print_success


@click.command("sqlite-to-excel")
@click.argument("db_path", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=None,
    help="Output Excel file path (default: same name as DB with .xlsx extension).",
)
def sqlite_to_excel(db_path: str, output: str | None) -> None:
    """Convert SQLite database to Excel.

    Each table in the database becomes a separate worksheet.

    Example: nf utils sqlite-to-excel metrics.db
    """
    db_file = Path(db_path)
    output_file = db_file.with_suffix(".xlsx") if not output else Path(output)

    print_info(f"Converting {db_file} to Excel...")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        if not tables:
            print_error("No tables found in database")
            return

        wb = Workbook()
        # Remove default sheet
        default_sheet = wb.active
        if default_sheet:
            wb.remove(default_sheet)

        for table in tables:
            print_info(f"  Processing table: {table}")

            # Get column names
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]

            # Get data
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()

            # Create worksheet
            ws = wb.create_sheet(title=table[:31])  # Excel limits sheet names to 31 chars
            ws.append(columns)
            for row in rows:
                ws.append(row)

        conn.close()

        wb.save(output_file)
        print_success(f"Saved to {output_file}")

    except Exception as e:
        print_error(f"Conversion failed: {e}")
