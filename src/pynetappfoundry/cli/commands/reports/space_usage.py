"""Generate space usage reports.

Creates Excel workbooks with 3 worksheets:
- Totals: Summary with SUMIFS formulas for licensing by cloud/cluster type/data type
- Usage Breakdown: Hierarchical breakdown with SUMIFS formulas referencing Volumes
- Volumes: Per-volume data with all metadata
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import click
import xlsxwriter
import xlsxwriter.utility

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_error, print_info, print_success
from pynetappfoundry.core.config import Config
from pynetappfoundry.utils.size import approximate_size_specific


class SpaceUsageReport:
    """Builds space usage Excel report matching sysadmin script layout."""

    def __init__(self, config: Config, clusters: dict[str, dict[str, Any]]) -> None:
        """Initialize the report builder."""
        self.config = config
        self.cluster_details = clusters
        self.volume_data: list[list[Any]] = []
        self.divisions: dict[str, Any] = {}

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = config.output_dir / f"space_usage_{timestamp}.xlsx"

        self.workbook = xlsxwriter.Workbook(str(self.filename))
        self.totals_ws = self.workbook.add_worksheet("Totals")
        self.usage_ws = self.workbook.add_worksheet("Usage Breakdown")
        self.volumes_ws = self.workbook.add_worksheet("Volumes")

        self._setup_formats()
        self._build_hierarchy()

    def _setup_formats(self) -> None:
        """Set up cell formats."""
        self.cell_format = self.workbook.add_format({"font_name": "Cascadia Mono", "font_size": 10})
        self.cell_format_number = self.workbook.add_format(
            {"font_name": "Cascadia Mono", "font_size": 10}
        )
        self.cell_format_number.set_num_format("0.00000")
        self.cell_format_red = self.workbook.add_format(
            {"font_name": "Cascadia Mono", "font_size": 10}
        )
        self.cell_format_red.set_bg_color("red")
        self.cell_format_red.set_font_color("white")
        self.cell_format_percentage = self.workbook.add_format(
            {"font_name": "Cascadia Mono", "font_size": 10}
        )
        self.cell_format_percentage.set_num_format("0.00%")

    def _build_hierarchy(self) -> None:
        """Build the divisions hierarchy from cluster details."""
        for item in self.cluster_details:
            details = self.cluster_details[item]
            div = details.get("div", "")
            bu = details.get("bu", "")
            app = details.get("app", "")
            env = details.get("env", "")
            subapp = details.get("subapp", "")
            cloud = details.get("cloud", "")
            region = details.get("region", "")

            if div not in self.divisions:
                self.divisions[div] = {}
            if bu not in self.divisions[div]:
                self.divisions[div][bu] = {}
            if app not in self.divisions[div][bu]:
                self.divisions[div][bu][app] = {}
            if env not in self.divisions[div][bu][app]:
                self.divisions[div][bu][app][env] = {}
            if subapp not in self.divisions[div][bu][app][env]:
                self.divisions[div][bu][app][env][subapp] = {}
            if cloud not in self.divisions[div][bu][app][env][subapp]:
                self.divisions[div][bu][app][env][subapp][cloud] = {}
            if region not in self.divisions[div][bu][app][env][subapp][cloud]:
                self.divisions[div][bu][app][env][subapp][cloud][region] = {
                    "CVO HA": {"RW": False, "DP": False},
                    "CVO": {"RW": False, "DP": False},
                }

    def gather_data(self) -> None:
        """Gather data from all clusters."""
        from netapp_ontap.host_connection import HostConnection
        from netapp_ontap.resources import Node, Volume

        for name, details in self.cluster_details.items():
            print_info(f"Gathering data for {name}...")
            user, password = self.config.get_user("clusters", name)

            try:
                with HostConnection(
                    details["ip"],
                    username=user,
                    password=password,
                    verify=False,
                ):
                    # Detect cluster type
                    nodes = list(Node.get_collection(fields="ha"))
                    if len(nodes) > 1 and nodes[0]["ha"]["enabled"]:
                        cluster_type = "CVO HA"
                    else:
                        cluster_type = "CVO"

                    # Get volumes (exclude SVM root volumes)
                    volumes = list(Volume.get_collection(is_svm_root=False, fields="*"))

                    div = details.get("div", "")
                    bu = details.get("bu", "")
                    app = details.get("app", "")
                    env = details.get("env", "")
                    subapp = details.get("subapp", "")
                    cloud = details.get("cloud", "")
                    region = details.get("region", "")
                    tags = details.get("tags", [])

                    for volume in volumes:
                        vol_size = volume["size"]
                        size_tib = float(
                            f"{approximate_size_specific(vol_size, 'TiB', withsuffix=False):.7f}"
                        )

                        if volume["state"] == "offline":
                            used_tib = 0.0
                        else:
                            used_bytes = volume["space"]["used"]
                            size_val = approximate_size_specific(
                                used_bytes, "TiB", withsuffix=False
                            )
                            used_tib = float(f"{size_val:.7f}")

                        data_type = volume["type"].upper()

                        # Mark this combination as having data
                        self.divisions[div][bu][app][env][subapp][cloud][region][cluster_type][
                            data_type
                        ] = True

                        # Calculate percent used
                        if size_tib > 0:
                            percent_used = float(f"{(used_tib / size_tib) * 100:.3f}")
                        else:
                            percent_used = 0.0

                        self.volume_data.append(
                            [
                                div,
                                bu,
                                name,
                                app,
                                env,
                                subapp,
                                cloud,
                                region,
                                cluster_type,
                                data_type,
                                volume["name"],
                                volume["state"],
                                ",".join(tags) if tags else "",
                                size_tib,
                                used_tib,
                                percent_used,
                            ]
                        )

            except Exception as e:
                print_error(f"Could not retrieve data for {name}: {e}")
                logging.error(f"Could not retrieve data for {name}: {e}", exc_info=e)

    def build_volumes_sheet(self) -> None:
        """Build the Volumes worksheet."""
        provision_col_header = "Provisioned (Licensing) TiB"
        used_col_header = "Used TiB"
        percentused_header = "%% Used"
        percentused_formula = f"=[@[{used_col_header}]]/[@[{provision_col_header}]] * 100"

        columns: list[dict[str, Any]] = [
            {"header": "Division", "total_string": ""},
            {"header": "BU", "total_string": ""},
            {"header": "Cluster", "total_string": ""},
            {"header": "App", "total_string": ""},
            {"header": "Environment", "total_string": ""},
            {"header": "SubApp", "total_string": ""},
            {"header": "Cloud", "total_string": ""},
            {"header": "Region", "total_string": ""},
            {"header": "Cluster Type", "total_string": ""},
            {"header": "Data Type", "total_string": ""},
            {"header": "Volume", "total_string": ""},
            {"header": "State", "total_string": ""},
            {"header": "Tags", "total_string": ""},
            {"header": provision_col_header, "total_function": "sum"},
            {"header": used_col_header, "total_function": "sum"},
            {
                "header": percentused_header,
                "formula": percentused_formula,
                "total_function": "average",
                "format": self.cell_format_number,
            },
        ]

        number_format = [provision_col_header, used_col_header, percentused_header]

        # Write headers
        for col_num, header in enumerate(columns):
            self.volumes_ws.write(0, col_num, header["header"], self.cell_format)

        # Write data and track max column width
        volumes_col_widths = [len(header["header"]) + 1 for header in columns]
        for row_num, row_data in enumerate(self.volume_data, start=1):
            for col_num, cell in enumerate(row_data):
                cell_format = self.cell_format
                if columns[col_num]["header"] in number_format:
                    cell_format = self.cell_format_number
                self.volumes_ws.write(row_num, col_num, cell, cell_format)
                cell_length = len(str(cell))
                if cell_length > volumes_col_widths[col_num]:
                    volumes_col_widths[col_num] = cell_length

        # Add table
        last_column = xlsxwriter.utility.xl_col_to_name(len(columns) - 1)
        table_range = f"A1:{last_column}{len(self.volume_data) + 2}"
        self.volumes_ws.add_table(
            table_range,
            {
                "columns": columns,
                "style": "Table Style Medium 9",
                "autofilter": True,
                "total_row": True,
                "name": "volume_table",
            },
        )  # pyright: ignore[reportCallIssue]

        # Auto-size columns
        for col_num, width in enumerate(volumes_col_widths):
            self.volumes_ws.set_column(col_num, col_num, width + 4)

        # Conditional formatting for high usage
        self.volumes_ws.conditional_format(
            f"{last_column}2:{last_column}{len(self.volume_data) + 1}",
            {
                "type": "cell",
                "criteria": ">=",
                "value": 90,
                "format": self.cell_format_red,
            },
        )  # pyright: ignore[reportCallIssue]

    def build_usage_sheet(self) -> None:
        """Build the Usage Breakdown worksheet with SUMIFS formulas."""
        provision_col_header = "Provisioned (Licensing) TiB"
        used_col_header = "Used TiB"
        numbers_format = [provision_col_header, used_col_header, "% Used"]

        percentused_formula = f"=[@[{used_col_header}]]/[@[{provision_col_header}]] * 100"
        columns: list[dict[str, Any]] = [
            {"header": "Division", "total_string": ""},
            {"header": "BU", "total_string": ""},
            {"header": "App", "total_string": ""},
            {"header": "Environment", "total_string": ""},
            {"header": "SubApp", "total_string": ""},
            {"header": "Cloud", "total_string": ""},
            {"header": "Region", "total_string": ""},
            {"header": "Cluster Type", "total_string": ""},
            {"header": "Data Type", "total_string": ""},
            {"header": provision_col_header, "total_function": "sum"},
            {"header": used_col_header, "total_function": "sum"},
            {
                "header": "% Used",
                "formula": percentused_formula,
                "total_function": "average",
                "format": self.cell_format_number,
            },
        ]

        volume_last_row = len(self.volume_data) + 1
        usage_data: list[list[Any]] = []

        # Write headers
        for col_num, header in enumerate(columns):
            self.usage_ws.write(0, col_num, header["header"], self.cell_format)

        # Build usage data with SUMIFS formulas
        for div in self.divisions:
            for bu in self.divisions[div]:
                for app in self.divisions[div][bu]:
                    for env in self.divisions[div][bu][app]:
                        for subapp in self.divisions[div][bu][app][env]:
                            for cloud in self.divisions[div][bu][app][env][subapp]:
                                for region in self.divisions[div][bu][app][env][subapp][cloud]:
                                    for cluster_type in self.divisions[div][bu][app][env][subapp][
                                        cloud
                                    ][region]:
                                        for data_type in self.divisions[div][bu][app][env][subapp][
                                            cloud
                                        ][region][cluster_type]:
                                            if self.divisions[div][bu][app][env][subapp][cloud][
                                                region
                                            ][cluster_type][data_type]:
                                                func_filter = (
                                                    f'Volumes!$A$2:$A${volume_last_row},"{div}",'
                                                    f'Volumes!$B$2:$B${volume_last_row},"{bu}",'
                                                    f'Volumes!$D$2:$D${volume_last_row},"{app}",'
                                                    f'Volumes!$E$2:$E${volume_last_row},"{env}",'
                                                    f'Volumes!$F$2:$F${volume_last_row},"{subapp}",'
                                                    f'Volumes!$G$2:$G${volume_last_row},"{cloud}",'
                                                    f'Volumes!$H$2:$H${volume_last_row},"{region}",'
                                                    f'Volumes!$I$2:$I${volume_last_row},"{cluster_type}",'
                                                    f'Volumes!$J$2:$J${volume_last_row},"{data_type}")'
                                                )
                                                usage_data.append(
                                                    [
                                                        div,
                                                        bu,
                                                        app,
                                                        env,
                                                        subapp,
                                                        cloud,
                                                        region,
                                                        cluster_type,
                                                        data_type,
                                                        f"=SUMIFS(Volumes!$N$2:$N${volume_last_row},{func_filter}",
                                                        f"=SUMIFS(Volumes!$O$2:$O${volume_last_row},{func_filter}",
                                                        "",
                                                    ]
                                                )

        # Write data and track max column width
        usage_col_widths = [len(header["header"]) + 1 for header in columns]
        for row_num, row_data in enumerate(usage_data, start=1):
            for col_num, cell in enumerate(row_data):
                cell_format = self.cell_format
                if columns[col_num]["header"] in numbers_format:
                    cell_format = self.cell_format_number
                self.usage_ws.write(row_num, col_num, cell, cell_format)
                cell_length = len(str(cell))
                if (not str(cell).startswith("=")) and cell_length > usage_col_widths[col_num]:
                    usage_col_widths[col_num] = cell_length

        # Add table
        last_column = xlsxwriter.utility.xl_col_to_name(len(columns) - 1)
        table_range = f"A1:{last_column}{len(usage_data) + 2}"
        self.usage_ws.add_table(
            table_range,
            {
                "columns": columns,
                "style": "Table Style Medium 9",
                "autofilter": True,
                "total_row": True,
                "name": "usage_table",
            },
        )  # pyright: ignore[reportCallIssue]

        # Auto-size columns and find % Used column
        percentused_column = ""
        for col_num, width in enumerate(usage_col_widths):
            self.usage_ws.set_column(col_num, col_num, width + 2)
            if columns[col_num]["header"] == "% Used":
                percentused_column = xlsxwriter.utility.xl_col_to_name(col_num)

        # Conditional formatting for high usage
        self.usage_ws.conditional_format(
            f"{percentused_column}2:{percentused_column}{len(usage_data) + 2}",
            {
                "type": "cell",
                "criteria": ">=",
                "value": 90,
                "format": self.cell_format_red,
            },
        )  # pyright: ignore[reportCallIssue]

    def build_totals_sheet(self) -> None:
        """Build the Totals worksheet with SUMIFS formulas."""
        # Headers
        self.totals_ws.write("A1", "Type")  # pyright: ignore[reportArgumentType]
        self.totals_ws.set_column(0, 0, 17)
        self.totals_ws.write(  # pyright: ignore[reportArgumentType]
            "B1", "Total Provisioned (Licensing) (TiB)"
        )
        self.totals_ws.set_column(1, 1, 31.5)
        self.totals_ws.write("C1", "Used (TiB)")  # pyright: ignore[reportArgumentType]
        self.totals_ws.set_column(2, 2, 14)
        self.totals_ws.write("D1", "Percent Used")  # pyright: ignore[reportArgumentType]
        self.totals_ws.set_column(3, 3, 13)

        # Azure CVO RW
        self.totals_ws.write("A2", "Azure CVO RW")  # pyright: ignore[reportArgumentType]
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "B2",
            formula=(
                "=SUMIFS(usage_table[Provisioned (Licensing) TiB],"
                'usage_table[Cloud],"azure",usage_table[Cluster Type],'
                '"CVO",usage_table[Data Type],"RW")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "C2",
            formula=(
                '=SUMIFS(usage_table[Used TiB],usage_table[Cloud],"azure",'
                'usage_table[Cluster Type],"CVO",usage_table[Data Type],"RW")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "D2",
            formula="=IFERROR($C$2/$B$2, 0)",
            cell_format=self.cell_format_percentage,
        )

        # Azure CVO DP
        self.totals_ws.write("A3", "Azure CVO DP")  # pyright: ignore[reportArgumentType]
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "B3",
            formula=(
                "=SUMIFS(usage_table[Provisioned (Licensing) TiB],"
                'usage_table[Cloud],"azure",usage_table[Cluster Type],'
                '"CVO",usage_table[Data Type],"DP")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "C3",
            formula=(
                "=SUMIFS(usage_table[Used TiB],usage_table[Cloud],"
                '"azure",usage_table[Cluster Type],"CVO",'
                'usage_table[Data Type],"DP")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "D3",
            formula="=IFERROR($C$3/$B$3, 0)",
            cell_format=self.cell_format_percentage,
        )

        # Azure CVO HA RW
        self.totals_ws.write(  # pyright: ignore[reportArgumentType]
            "A4", "Azure CVO HA RW"
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "B4",
            formula=(
                "=SUMIFS(usage_table[Provisioned (Licensing) TiB],"
                'usage_table[Cloud],"azure",usage_table[Cluster Type],"CVO HA",'
                'usage_table[Data Type],"RW")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "C4",
            formula=(
                "=SUMIFS(usage_table[Used TiB],usage_table[Cloud],"
                '"azure",usage_table[Cluster Type],"CVO HA",'
                'usage_table[Data Type],"RW")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "D4",
            formula="=IFERROR($C$4/$B$4, 0)",
            cell_format=self.cell_format_percentage,
        )

        # Azure CVO HA DP
        self.totals_ws.write(  # pyright: ignore[reportArgumentType]
            "A5", "Azure CVO HA DP"
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "B5",
            formula=(
                "=SUMIFS(usage_table[Provisioned (Licensing) TiB],"
                'usage_table[Cloud],"azure",usage_table[Cluster Type],'
                '"CVO HA",usage_table[Data Type],"DP")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "C5",
            formula=(
                "=SUMIFS(usage_table[Used TiB],usage_table[Cloud],"
                '"azure",usage_table[Cluster Type],"CVO HA",'
                'usage_table[Data Type],"DP")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "D5",
            formula="=IFERROR($C$5/$B$5, 0)",
            cell_format=self.cell_format_percentage,
        )

        # Azure Totals
        self.totals_ws.write("A6", "Azure Totals")  # pyright: ignore[reportArgumentType]
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "B6", formula="=SUM($B2:$B5)", cell_format=self.cell_format_number
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "C6", formula="=SUM($C2:$C5)", cell_format=self.cell_format_number
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "D6",
            formula="=IFERROR($C$6/$B$6, 0)",
            cell_format=self.cell_format_percentage,
        )

        # AWS CVO RW
        self.totals_ws.write("A8", "AWS CVO RW")  # pyright: ignore[reportArgumentType]
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "B8",
            formula=(
                "=SUMIFS(usage_table[Provisioned (Licensing) TiB],"
                'usage_table[Cloud],"aws",usage_table[Cluster Type],"CVO",'
                'usage_table[Data Type],"RW")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "C8",
            formula=(
                '=SUMIFS(usage_table[Used TiB],usage_table[Cloud],"aws",'
                'usage_table[Cluster Type],"CVO",usage_table[Data Type],"RW")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "D8",
            formula="=IFERROR($C$8/$B$8, 0)",
            cell_format=self.cell_format_percentage,
        )

        # AWS CVO DP
        self.totals_ws.write("A9", "AWS CVO DP")  # pyright: ignore[reportArgumentType]
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "B9",
            formula=(
                "=SUMIFS(usage_table[Provisioned (Licensing) TiB],"
                'usage_table[Cloud],"aws",usage_table[Cluster Type],"CVO",'
                'usage_table[Data Type],"DP")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "C9",
            formula=(
                "=SUMIFS(usage_table[Used TiB],usage_table[Cloud],"
                '"aws",usage_table[Cluster Type],"CVO",usage_table[Data Type],"DP")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "D9",
            formula="=IFERROR($C$9/$B$9, 0)",
            cell_format=self.cell_format_percentage,
        )

        # AWS CVO HA RW
        self.totals_ws.write(  # pyright: ignore[reportArgumentType, reportCallIssue]
            "A10", "AWS CVO HA RW"
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "B10",
            formula=(
                "=SUMIFS(usage_table[Provisioned (Licensing) TiB],"
                'usage_table[Cloud],"aws",usage_table[Cluster Type],'
                '"CVO HA",usage_table[Data Type],"RW")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "C10",
            formula=(
                "=SUMIFS(usage_table[Used TiB],usage_table[Cloud],"
                '"aws",usage_table[Cluster Type],"CVO HA",usage_table[Data Type],"RW")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "D10",
            formula="=IFERROR($C$10/$B$10, 0)",
            cell_format=self.cell_format_percentage,
        )

        # AWS CVO HA DP
        self.totals_ws.write(  # pyright: ignore[reportArgumentType, reportCallIssue]
            "A11", "AWS CVO HA DP"
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "B11",
            formula=(
                "=SUMIFS(usage_table[Provisioned (Licensing) TiB],"
                'usage_table[Cloud],"aws",usage_table[Cluster Type],'
                '"CVO HA",usage_table[Data Type],"DP")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "C11",
            formula=(
                "=SUMIFS(usage_table[Used TiB],usage_table[Cloud],"
                '"aws",usage_table[Cluster Type],"CVO HA",usage_table[Data Type],"DP")'
            ),
            cell_format=self.cell_format_number,
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "D11",
            formula="=IFERROR($C$11/$B$11, 0)",
            cell_format=self.cell_format_percentage,
        )

        # AWS Totals
        self.totals_ws.write("A12", "AWS Totals")  # pyright: ignore[reportArgumentType]
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "B12", formula="=SUM($B8:$B11)", cell_format=self.cell_format_number
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "C12", formula="=SUM($C8:$C11)", cell_format=self.cell_format_number
        )
        self.totals_ws.write_formula(  # pyright: ignore[reportCallIssue]
            "D12",
            formula="=IFERROR($C$12/$B$12, 0)",
            cell_format=self.cell_format_percentage,
        )

    def generate(self) -> None:
        """Generate the complete report."""
        self.gather_data()

        if not self.volume_data:
            print_error("No volume data collected. Check cluster connectivity.")
            self.workbook.close()
            return

        self.build_volumes_sheet()
        self.build_usage_sheet()
        self.build_totals_sheet()

        self.workbook.close()
        print_success(f"Report saved to {self.filename}")


@click.command("space-usage")
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@with_config("Space usage report failed")
def space_usage(
    config: Config,
    clusters: dict[str, dict[str, Any]],
) -> None:
    """Generate space usage reports.

    Creates an Excel workbook with 3 worksheets:
    - Totals: Summary by cloud provider, cluster type, and data type
    - Usage Breakdown: Hierarchical breakdown with SUMIFS formulas
    - Volumes: Per-volume data with state, tags, and conditional formatting
    """
    report = SpaceUsageReport(config, clusters)
    report.generate()
