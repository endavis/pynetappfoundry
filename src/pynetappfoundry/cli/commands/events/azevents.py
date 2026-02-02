"""Save Azure maintenance events from EMS event stream."""

from __future__ import annotations

import re
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

    # Required fields for CVO (non-HA) clusters
    CVO_REQUIRED_FIELDS: ClassVar[list[str]] = [
        "az_maint_not_before",
        "az_maint_scheduled",
        "az_maint_started",
        "az_maint_complete",
    ]

    # Additional fields required for CVO HA clusters
    CVO_HA_ADDITIONAL_FIELDS: ClassVar[list[str]] = [
        "node_takeover_complete",
        "node_reboot_starts",
        "node_reboot_complete",
        "node_ready_for_giveback",
        "node_giveback_starts",
        "node_giveback_complete",
    ]

    # SMB client impact events for CVO HA clusters
    SMB_IMPACT_EVENTS: ClassVar[list[str]] = [
        "vifmgr.lifBeingRemoved",
        "vifmgr.lifsuccessfullymoved",
        "Nblade.cifsWitnessFONotify",
        "cf.transition.info",
        "ha.sfo.giveback.aggrStart",
        "ha.sfo.giveback.aggrDone",
    ]

    # SMB client impact fields for CVO HA clusters (optional - may not always be present)
    CVO_HA_SMB_FIELDS: ClassVar[list[str]] = [
        "lif_failover_start",
        "lif_failover_complete",
        "cifs_transition_ms",
        "cifs_witness_time",
        "cifs_witness_clients",
        "aggr_giveback_start",
        "aggr_giveback_complete",
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

    def _add_emsevent(self, emsevent: Any) -> None:
        """Add an EMS event to the tracking list.

        Args:
            emsevent: EMS event resource object from API (not converted to dict).
        """
        event_name = emsevent["message"]["name"]
        message = emsevent["log_message"]
        # Clean up message
        message = message.replace(f"{event_name}: ", "").replace(",", ";").replace("\n", "").strip()

        event_dict = {
            "event_id": self.current_azevent,
            "cluster": self.name,
            "node": emsevent["node"]["name"],
            "time": emsevent["time"],
            "event": event_name,
            "severity": emsevent["message"]["severity"],
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
        """Save all collected EMS events to a separate database for debugging.

        When a maintenance event has missing fields or other problems, this saves
        ALL EMS events from the cluster to a debug database so you can manually
        trace through the event sequence to understand what went wrong.

        Args:
            db_name: Name for the error database file.
        """
        emsdb = EmsEventsDB(config=self.config, db_name=db_name, overwrite=False)
        if emsdb.exists:
            print_info(f"Debug database {db_name} already exists, skipping")
            return

        for emsevent in self.ems_events:
            emsdb.insert_event(emsevent)
        emsdb.conn.close()
        print_info(f"Saved {len(self.ems_events)} EMS events to {db_name} for debugging")

    def _get_param_value(self, parameters: list[Any], param_name: str) -> str | None:
        """Extract a parameter value from EMS event parameters.

        Args:
            parameters: List of parameter objects with 'name' and 'value'.
            param_name: Parameter name to find.

        Returns:
            Parameter value or None if not found.
        """
        # Use item["name"] instead of item.get("name") because EmsEventParameter
        # objects support [] access but not .get()
        return next(
            (item["value"] for item in parameters if item["name"] == param_name),
            None,
        )

    def _parse_cifs_transition_ms(self, log_message: str) -> int | None:
        """Extract CIFS transition time in milliseconds from cf.transition.info.

        Args:
            log_message: Log message containing protocol transition times.
                         Format: "CIFS=14450[210|14240]"

        Returns:
            CIFS transition time in milliseconds, or None if not found.
        """
        # Match CIFS=<number> pattern
        match = re.search(r"CIFS=(\d+)", log_message)
        if match:
            return int(match.group(1))
        return None

    def _parse_cifs_witness_info(self, log_message: str) -> tuple[int | None, int | None]:
        """Extract CIFS Witness notification info from Nblade.cifsWitnessFONotify.

        Args:
            log_message: Log message containing witness notification details.
                         Format: "Notification of X CIFS clients...took Y milliseconds"

        Returns:
            Tuple of (client_count, notification_ms), or (None, None) if not parsed.
        """
        client_count = None
        notification_ms = None

        # Match "Notification of X CIFS clients"
        client_match = re.search(r"Notification of (\d+) CIFS clients", log_message)
        if client_match:
            client_count = int(client_match.group(1))

        # Match "took X milliseconds"
        ms_match = re.search(r"took (\d+) milliseconds", log_message)
        if ms_match:
            notification_ms = int(ms_match.group(1))

        return client_count, notification_ms

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
                    self._add_emsevent(emsevent)

                    message_name = emsevent["message"]["name"]

                    # Extract common parameters for vsa.scheduled events
                    if "vsa.scheduled" in message_name:
                        # Only access parameters for events that need them
                        try:
                            parameters = emsevent["parameters"]
                        except KeyError:
                            print_warning(
                                f"{self.name}: Event {message_name} missing parameters field"
                            )
                            parameters = []
                        print_debug(f"Found vsa.scheduled: {emsevent.to_dict()}")
                        azevent_id = self._get_param_value(parameters, "event_id")
                        event_type = self._get_param_value(parameters, "event_type")
                        node = self._get_param_value(parameters, "node")
                        status = self._get_param_value(parameters, "status")
                        not_before_time = self._get_param_value(parameters, "not_before_time")

                    # Process events based on message name
                    match message_name:
                        case "vsa.scheduledEvent.scheduled":
                            print_debug(f"Found vsa.scheduledEvent.scheduled: {emsevent.to_dict()}")
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
                                azevent_dict["az_maint_scheduled"] = emsevent["time"]
                                self.current_azevent = azevent_id or ""
                            except Exception:
                                self.current_azevent = "Unknown"
                                print_error(
                                    f"Got an invalid maintenance event: {emsevent.to_dict()}"
                                )
                                self.invalid_maintenance = True

                        case "vsa.scheduledEvent.update":
                            print_debug(f"Found vsa.scheduledEvent.update: {emsevent.to_dict()}")
                            # Handle out-of-order events
                            if azevent_id != azevent_dict["event_id"]:
                                print_warning(
                                    f"{self.name}: Out of order az event - "
                                    f"tracking {azevent_dict['event_id']}, "
                                    f"received update for {azevent_id}"
                                )
                                print_debug(f"Current Event details: {azevent_dict}")
                                print_debug(f"Full current EMS details: {emsevent.to_dict()}")
                                self._add_azmaint(azevent_dict)
                                self._empty_azevent()
                                # Check if this event already exists (e.g., callhome.reboot.giveback
                                # came before vsa.scheduledEvent.update complete)
                                if azevent_id and azevent_id in self.azmaints:
                                    # Update existing event with status
                                    status_field = f"az_maint_{status}"
                                    self.azmaints[azevent_id][status_field] = emsevent["time"]
                                    print_debug(f"Updated event {azevent_id} with {status_field}")
                                elif azevent_dict["event_id"] == "Unknown":
                                    azevent_dict["event_id"] = azevent_id
                                    azevent_dict["node"] = node
                                    azevent_dict["type"] = event_type
                            else:
                                # Record started/complete status
                                azevent_dict[f"az_maint_{status}"] = emsevent["time"]

                            # For non-HA CVO, complete on az_maint_complete
                            if status == "complete" and self.cluster_type == "CVO":
                                self._add_azmaint(azevent_dict)
                                azevent_dict = self._empty_azevent()

                        case "cf.fsm.nfo.startingGracefulShutdown":
                            # Takeover complete
                            azevent_dict["node_takeover_complete"] = emsevent["time"]

                        case "kern.shutdown":
                            # Node starts rebooting
                            azevent_dict["node_reboot_starts"] = emsevent["time"]

                        case "mgr.boot.disk_done":
                            # Node finished rebooting
                            azevent_dict["node_reboot_complete"] = emsevent["time"]

                        case "cf.fsm.takeoverOfPartnerEnabled":
                            # Node ready for giveback
                            azevent_dict["node_ready_for_giveback"] = emsevent["time"]

                        case "clam.valid.config":
                            # Giveback starts
                            azevent_dict["node_giveback_starts"] = emsevent["time"]

                        # SMB client impact events
                        case "vifmgr.lifBeingRemoved":
                            # LIF failover starts - track first occurrence only
                            if "lif_failover_start" not in azevent_dict:
                                azevent_dict["lif_failover_start"] = emsevent["time"]

                        case "vifmgr.lifsuccessfullymoved":
                            # LIF successfully moved - track last occurrence
                            azevent_dict["lif_failover_complete"] = emsevent["time"]

                        case "Nblade.cifsWitnessFONotify":
                            # CIFS Witness failover notification
                            azevent_dict["cifs_witness_time"] = emsevent["time"]
                            client_count, _ = self._parse_cifs_witness_info(emsevent["log_message"])
                            if client_count is not None:
                                azevent_dict["cifs_witness_clients"] = client_count

                        case "cf.transition.info":
                            # Protocol transition times - extract CIFS ms
                            cifs_ms = self._parse_cifs_transition_ms(emsevent["log_message"])
                            if cifs_ms is not None:
                                azevent_dict["cifs_transition_ms"] = cifs_ms

                        case "ha.sfo.giveback.aggrStart":
                            # Aggregate giveback started - track first occurrence only
                            if "aggr_giveback_start" not in azevent_dict:
                                azevent_dict["aggr_giveback_start"] = emsevent["time"]

                        case "ha.sfo.giveback.aggrDone":
                            # Aggregate giveback completed - track last occurrence
                            azevent_dict["aggr_giveback_complete"] = emsevent["time"]

                        case "callhome.reboot.giveback":
                            # Event complete - giveback finished (HA completion marker)
                            azevent_dict["node_giveback_complete"] = emsevent["time"]
                            azevent_id = azevent_dict["event_id"]
                            if azevent_id == "Unknown":
                                print_error(f"{self.name}: No Event Id for {azevent_dict}")
                            else:
                                # Add EMS event before resetting current_azevent
                                self._add_emsevent(emsevent)
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

    def _get_missing_fields(self, event_row: dict[str, Any]) -> list[str]:
        """Get list of missing required fields for an event.

        Args:
            event_row: Event dictionary from database.

        Returns:
            List of field names that are empty/missing.
        """
        missing: list[str] = []

        # Check CVO required fields (always required)
        for field in self.CVO_REQUIRED_FIELDS:
            if event_row.get(field) in ("", None):
                missing.append(field)

        # Check CVO HA additional fields (only for HA clusters)
        if self.cluster_type == "CVO HA":
            for field in self.CVO_HA_ADDITIONAL_FIELDS:
                if event_row.get(field) in ("", None):
                    missing.append(field)

        return missing

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
                print_error(f"{self.name}: Event without id: {azevent}")
                self._save_emsevents(db_name)
            else:
                azevent_from_db = self.db.get_event_by_id(azevent["event_id"])
                if azevent_from_db is None:
                    continue

                azevent_row = dict(azevent_from_db)
                missing_fields = self._get_missing_fields(azevent_row)

                if missing_fields:
                    db_name = (
                        f"{self.name}_{azevent_row['event_id']}"
                        f"_missing_{self.dt_now:%d-%m-%Y-%H-%M-%S}.db"
                    )
                    print_error(
                        f"{self.name}: Event {azevent_row['event_id']} "
                        f"for node {azevent_row.get('node', 'Unknown')} "
                        f"missing fields: {', '.join(missing_fields)}"
                    )
                    self._save_emsevents(db_name)
