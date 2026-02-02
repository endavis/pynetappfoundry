"""Save Azure maintenance events from EMS event stream."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, ClassVar

import click

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import (
    print_debug,
    print_error,
    print_info,
    print_success,
    print_warning,
)
from pynetappfoundry.db.azevents import AzEventsDB
from pynetappfoundry.db.ems import EmsEventsDB

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config


@click.command("save-azure")
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@with_config("Save Azure events failed")
def save_azure(
    config: Config,
    clusters: dict[str, dict[str, Any]],
) -> None:
    """Save Azure maintenance events to database.

    Parses EMS event stream to track complete maintenance lifecycle including
    Azure scheduled events, node takeover/giveback for HA clusters.
    """
    db = AzEventsDB(config)
    dt_now = datetime.now()

    for name, details in clusters.items():
        # Skip non-Azure clusters
        if details.get("cloud", "").lower() != "azure":
            continue

        print_info(f"Getting Azure events for {name}...")
        cluster_data = ClusterData(name, details, config, db, dt_now)
        cluster_data.gather_data()
        cluster_data.process_data()

    db.conn.close()
    print_success("Azure events saved to database")


class ClusterData:
    """Tracks maintenance event state for a single cluster."""

    # EMS events that indicate various maintenance lifecycle stages
    SCHEDULED_EVENTS: ClassVar[list[str]] = [
        "vsa.scheduledEvent.scheduled",
        "vsa.scheduledEvent.update",
    ]

    def __init__(
        self,
        name: str,
        details: dict[str, Any],
        config: Config,
        db: AzEventsDB,
        dt_now: datetime,
    ) -> None:
        """Initialize cluster data tracker.

        Args:
            name: Cluster name.
            details: Cluster connection details.
            config: Configuration object.
            db: Azure events database.
            dt_now: Current datetime for error db naming.
        """
        self.name = name
        self.details = details
        self.config = config
        self.db = db
        self.dt_now = dt_now
        self.cluster_type = ""
        self.current_azevent = ""
        self.invalid_maintenance = False
        self.azmaints: dict[str, dict[str, Any]] = {}
        self.ems_events: list[dict[str, Any]] = []

    def _empty_azevent(self) -> dict[str, Any]:
        """Create an empty Azure event dict and reset current event tracking.

        Returns:
            Empty event dict with Unknown event_id.
        """
        self.current_azevent = ""
        return {"event_id": "Unknown"}

    def _add_emsevent(self, emsevent: dict[str, Any]) -> None:
        """Add an EMS event to the tracking list.

        Args:
            emsevent: EMS event dictionary from API.
        """
        message = emsevent.get("log_message", "")
        event_name = emsevent.get("message", {}).get("name", "")
        # Clean up message
        message = message.replace(f"{event_name}: ", "").replace(",", ";").replace("\n", "").strip()

        event_dict = {
            "event_id": self.current_azevent,
            "cluster": self.name,
            "node": emsevent.get("node", {}).get("name", "Unknown"),
            "time": emsevent.get("time"),
            "event": event_name,
            "severity": emsevent.get("message", {}).get("severity", "Unknown"),
            "message": message,
        }
        self.ems_events.append(event_dict)

    def _add_azmaint(self, azmaint: dict[str, Any]) -> None:
        """Add or update an Azure maintenance event.

        Args:
            azmaint: Azure maintenance event dictionary.
        """
        event_id = azmaint.get("event_id", "Unknown")
        if event_id in self.azmaints:
            self.azmaints[event_id].update(azmaint)
        else:
            self.azmaints[event_id] = azmaint
        self.current_azevent = ""

    def _save_emsevents(self, db_name: str) -> None:
        """Save EMS events to a separate database for debugging.

        Args:
            db_name: Name for the error database file.
        """
        import os

        db_path = self.config.db_dir / "emsevents" / db_name
        if os.path.exists(db_path):
            print_info(f"{db_name} already exists")
            return

        emsdb = EmsEventsDB(config=self.config, db_name=db_name, overwrite=False)
        if not emsdb.exists:
            for emsevent in self.ems_events:
                emsdb.insert_event(emsevent)
            emsdb.conn.close()
            print_error(f"All events saved to {db_name}")
        else:
            print_info(f"Events already saved to {db_name}")

    def _get_param_value(self, parameters: list[dict[str, Any]], param_name: str) -> str | None:
        """Extract a parameter value from EMS event parameters.

        Args:
            parameters: List of parameter dicts with 'name' and 'value'.
            param_name: Parameter name to find.

        Returns:
            Parameter value or None if not found.
        """
        return next(
            (item["value"] for item in parameters if item.get("name") == param_name),
            None,
        )

    def gather_data(self) -> None:
        """Gather and parse EMS events from the cluster."""
        import netapp_ontap.error
        from netapp_ontap import HostConnection  # pyright: ignore[reportPrivateImportUsage]
        from netapp_ontap.resources import EmsEvent, Node

        azevent_dict = self._empty_azevent()
        azevent_id: str | None = "Unknown"
        status: str | None = ""
        not_before_time: str | None = ""
        node: str | None = ""
        event_type: str | None = ""
        emsevent: Any = None

        try:
            user, password = self.config.get_user("clusters", self.name)
            with HostConnection(
                self.details["ip"],
                username=user,
                password=password,
                verify=False,
            ):
                # Detect CVO vs CVO HA
                nodes = list(Node.get_collection(fields="ha"))
                if len(nodes) > 1 and nodes[0].to_dict().get("ha", {}).get("enabled"):
                    self.cluster_type = "CVO HA"
                else:
                    self.cluster_type = "CVO"

                print_debug(f"{self.name} is {self.cluster_type}")

                # Check if any scheduled events exist
                scheduled_query: dict[str, Any] = {
                    "message.name": ",".join(self.SCHEDULED_EVENTS),
                    "order_by": "time",
                    "fields": "*",
                }
                scheduled = list(EmsEvent.get_collection(**scheduled_query))

                if len(scheduled) == 0:
                    print_info(f"{self.name}: No maintenance events")
                    return

                print_info(f"{self.name}: Found maintenance events")

                # Process all EMS events to track maintenance lifecycle
                all_events_query: dict[str, Any] = {
                    "message.severity": "*",
                    "order_by": "time",
                    "fields": "*",
                }
                for emsevent in EmsEvent.get_collection(**all_events_query):
                    emsevent_dict = emsevent.to_dict()
                    self._add_emsevent(emsevent_dict)

                    message_name = emsevent_dict.get("message", {}).get("name", "")
                    parameters = emsevent_dict.get("parameters", [])

                    # Extract common parameters for vsa.scheduled events
                    if "vsa.scheduled" in message_name:
                        print_debug(f"Found vsa.scheduled: {emsevent_dict}")
                        azevent_id = self._get_param_value(parameters, "event_id")
                        event_type = self._get_param_value(parameters, "event_type")
                        node = self._get_param_value(parameters, "node")
                        status = self._get_param_value(parameters, "status")
                        not_before_time = self._get_param_value(parameters, "not_before_time")

                    # Process events based on message name
                    match message_name:
                        case "vsa.scheduledEvent.scheduled":
                            print_debug(f"Found vsa.scheduledEvent.scheduled: {emsevent_dict}")
                            # Found a new event - check if previous wasn't completed
                            if azevent_dict["event_id"] != "Unknown":
                                print_warning(
                                    f"{self.name}: Could not find completion "
                                    f"for AZ event {azevent_dict['event_id']}"
                                )
                                self._add_azmaint(azevent_dict)
                                azevent_dict = self._empty_azevent()

                            # Parse the scheduled event
                            try:
                                if not_before_time:
                                    azevent_dict["az_maint_not_before"] = datetime.strptime(
                                        not_before_time,
                                        "%m/%d/%Y %H:%M:%S",
                                    ).replace(tzinfo=UTC)
                                azevent_dict["event_id"] = azevent_id
                                azevent_dict["node"] = node
                                azevent_dict["type"] = event_type
                                azevent_dict["cluster"] = self.name
                                azevent_dict["az_maint_scheduled"] = emsevent_dict.get("time")
                                self.current_azevent = azevent_id or ""
                            except Exception:
                                self.current_azevent = "Unknown"
                                print_error(f"Got an invalid maintenance event: {emsevent_dict}")
                                self.invalid_maintenance = True

                        case "vsa.scheduledEvent.update":
                            print_debug(f"Found vsa.scheduledEvent.update: {emsevent_dict}")
                            # Handle out-of-order events
                            if azevent_id != azevent_dict["event_id"]:
                                print_warning(
                                    f"{self.name}: Out of order az event - "
                                    f"tracking {azevent_dict['event_id']}, "
                                    f"received update for {azevent_id}"
                                )
                                print_debug(f"Current Event details: {azevent_dict}")
                                print_debug(f"Full current EMS details: {emsevent_dict}")
                                self._add_azmaint(azevent_dict)
                                self._empty_azevent()
                                if azevent_dict["event_id"] == "Unknown":
                                    azevent_dict["event_id"] = azevent_id
                                    azevent_dict["node"] = node
                                    azevent_dict["type"] = event_type
                            else:
                                # Record started/complete status
                                azevent_dict[f"az_maint_{status}"] = emsevent_dict.get("time")

                            # For non-HA CVO, complete on az_maint_complete
                            if status == "complete" and self.cluster_type == "CVO":
                                self._add_azmaint(azevent_dict)
                                azevent_dict = self._empty_azevent()

                        case "cf.fsm.nfo.startingGracefulShutdown":
                            # Takeover complete
                            azevent_dict["node_takeover_complete"] = emsevent_dict.get("time")

                        case "kern.shutdown":
                            # Node starts rebooting
                            azevent_dict["node_reboot_starts"] = emsevent_dict.get("time")

                        case "mgr.boot.disk_done":
                            # Node finished rebooting
                            azevent_dict["node_reboot_complete"] = emsevent_dict.get("time")

                        case "cf.fsm.takeoverOfPartnerEnabled":
                            # Node ready for giveback
                            azevent_dict["node_ready_for_giveback"] = emsevent_dict.get("time")

                        case "clam.valid.config":
                            # Giveback starts
                            azevent_dict["node_giveback_starts"] = emsevent_dict.get("time")

                        case "callhome.reboot.giveback":
                            # Event complete - giveback finished (HA completion marker)
                            azevent_dict["node_giveback_complete"] = emsevent_dict.get("time")
                            azevent_id = azevent_dict["event_id"]
                            if azevent_id == "Unknown":
                                print_error(f"{self.name}: No Event Id for {azevent_dict}")
                            else:
                                # Add EMS event before resetting current_azevent
                                self._add_emsevent(emsevent_dict)
                                self._add_azmaint(azevent_dict)
                            self.current_azevent = ""
                            azevent_dict = self._empty_azevent()

                # Check for incomplete event left on stack
                if azevent_dict["event_id"] != "Unknown":
                    print_warning(
                        f"{self.name}: Incomplete az event {azevent_dict['event_id']} "
                        f"for node {azevent_dict.get('node', 'Unknown')} left on stack"
                    )
                    print_debug(f"Event details: {azevent_dict}")
                    self._add_azmaint(azevent_dict)

        except netapp_ontap.error.NetAppRestError:
            print_error(f"{self.name}: Could not connect to API")
        except Exception as e:
            print_error(f"Could not retrieve events for {self.name}: {e}")
            if emsevent:
                print_debug(f"Last EMS event was: {emsevent}")

    def process_data(self) -> None:
        """Process collected maintenance events and save to database."""
        for azevent in self.azmaints.values():
            print_info(
                f"Cluster {self.name} adding {azevent['event_id']} "
                f"for node {azevent.get('node', 'Unknown')}"
            )
            self.db.upsert_event(azevent)

            if azevent["event_id"] == "Unknown":
                db_name = f"{self.name}_Unknown_{self.dt_now:%d-%m-%Y-%H-%M-%S}.db"
                print_error(f"Found an event without an id: {azevent}")
                self._save_emsevents(db_name)
            else:
                azevent_from_db = self.db.get_event_by_id(azevent["event_id"])
                if azevent_from_db is None:
                    continue

                azevent_row = dict(azevent_from_db)

                # Check for missing maintenance fields
                if (
                    azevent_row.get("az_maint_not_before") == ""
                    or azevent_row.get("az_maint_scheduled") == ""
                    or azevent_row.get("az_maint_started") == ""
                    or azevent_row.get("az_maint_complete") == ""
                ):
                    db_name = (
                        f"{self.name}_{azevent_row['event_id']}"
                        f"_nomaint_{self.dt_now:%d-%m-%Y-%H-%M-%S}.db"
                    )
                    print_error(f"Found an event without maintenance fields: {azevent_row}")
                    self._save_emsevents(db_name)

                # For CVO HA, check for missing failover fields
                elif self.cluster_type == "CVO HA" and any(
                    value == "" for value in azevent_row.values()
                ):
                    db_name = (
                        f"{self.name}_{azevent_row['event_id']}_missing_fields"
                        f"_{self.dt_now:%d-%m-%Y-%H-%M-%S}.db"
                    )
                    print_error(
                        f"Found a CVO HA maintenance event without "
                        f"failover/failback fields: {azevent_row}"
                    )
                    self._save_emsevents(db_name)
