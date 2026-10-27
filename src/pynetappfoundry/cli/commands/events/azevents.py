"""Save Azure maintenance events from EMS event stream."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, ClassVar

import click
import requests

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import (
    print_debug,
    print_error,
    print_info,
    print_success,
    print_warning,
)
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.core.models import ClusterConfig
from pynetappfoundry.db.azevents import AzEventsDB
from pynetappfoundry.db.ems import EmsEventsDB
from pynetappfoundry.models.ontap.cluster.nodes import OntapNodeResponse
from pynetappfoundry.models.ontap.support.ems.events import OntapEmsEventResponse
from pynetappfoundry.query import QuerySet

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.models.ontap.support.ems.events.model import (
        OntapEmsEventResponseParameter,
    )


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
        # Timing data from "Unknown" events, keyed by node name
        # Used when scheduled event aged out before callhome.reboot.giveback
        self.pending_timing: dict[str, dict[str, Any]] = {}

    def _empty_azevent(self) -> dict[str, Any]:
        """Create an empty Azure event dict and reset current event tracking.

        Returns:
            Empty event dict with Unknown event_id.
        """
        self.current_azevent = ""
        return {"event_id": "Unknown"}

    def _add_emsevent(self, emsevent: OntapEmsEventResponse) -> None:
        """Add an EMS event to the tracking list.

        Args:
            emsevent: EMS event from the API.
        """
        event_name = emsevent.message.name
        message = emsevent.log_message
        # Clean up message
        message = message.replace(f"{event_name}: ", "").replace(",", ";").replace("\n", "").strip()

        event_dict = {
            "event_id": self.current_azevent,
            "cluster": self.name,
            "node": emsevent.node.name,
            "time": datetime.fromisoformat(emsevent.time),
            "event": event_name,
            "severity": emsevent.message.severity,
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

    def _get_param_value(
        self, parameters: list[OntapEmsEventResponseParameter], param_name: str
    ) -> str | None:
        """Extract a parameter value from EMS event parameters.

        Args:
            parameters: EMS event parameters, each with a name and a value.
            param_name: Parameter name to find.

        Returns:
            Parameter value or None if not found.
        """
        return next(
            (item.value for item in parameters if item.name == param_name),
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
        azevent_dict = self._empty_azevent()
        azevent_id: str | None = "Unknown"
        status: str | None = ""
        not_before_time: str | None = ""
        node: str | None = ""
        event_type: str | None = ""
        emsevent: OntapEmsEventResponse | None = None

        try:
            client = ONTAPAPIClient(cluster=ClusterConfig(**self.details), config=self.config)
            # Detect CVO vs CVO HA
            nodes: list[OntapNodeResponse] = QuerySet(
                OntapNodeResponse, client, config=self.config
            ).all()
            if len(nodes) > 1 and nodes[0].ha.enabled:
                self.cluster_type = "CVO HA"
            else:
                self.cluster_type = "CVO"

            print_debug(f"{self.name} is {self.cluster_type}")

            # Check if any scheduled events exist
            scheduled: list[OntapEmsEventResponse] = (
                QuerySet(OntapEmsEventResponse, client, config=self.config)
                .filter(**{"message.name": ",".join(self.SCHEDULED_EVENTS)})
                .order_by("time")
                .all()
            )

            if len(scheduled) == 0:
                print_info(f"{self.name}: No maintenance events")
                return

            print_info(f"{self.name}: Found maintenance events")

            # Process all EMS events to track maintenance lifecycle
            all_events: list[OntapEmsEventResponse] = (
                QuerySet(OntapEmsEventResponse, client, config=self.config)
                .filter(**{"message.severity": "*"})
                .order_by("time")
                .all()
            )
            for emsevent in all_events:
                self._add_emsevent(emsevent)

                message_name = emsevent.message.name
                event_time = datetime.fromisoformat(emsevent.time)

                # Extract common parameters for vsa.scheduled events
                if "vsa.scheduled" in message_name:
                    # Only access parameters for events that need them
                    parameters = emsevent.parameters
                    if not parameters:
                        print_warning(f"{self.name}: Event {message_name} missing parameters field")
                    print_debug(f"Found vsa.scheduled: {emsevent.model_dump()}")
                    azevent_id = self._get_param_value(parameters, "event_id")
                    event_type = self._get_param_value(parameters, "event_type")
                    node = self._get_param_value(parameters, "node")
                    status = self._get_param_value(parameters, "status")
                    not_before_time = self._get_param_value(parameters, "not_before_time")

                # Process events based on message name
                match message_name:
                    case "vsa.scheduledEvent.scheduled":
                        print_debug(f"Found vsa.scheduledEvent.scheduled: {emsevent.model_dump()}")
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
                            azevent_dict["az_maint_scheduled"] = event_time
                            self.current_azevent = azevent_id or ""
                        except Exception:
                            self.current_azevent = "Unknown"
                            print_error(
                                f"Got an invalid maintenance event: {emsevent.model_dump()}"
                            )
                            self.invalid_maintenance = True

                    case "vsa.scheduledEvent.update":
                        print_debug(f"Found vsa.scheduledEvent.update: {emsevent.model_dump()}")
                        # Handle out-of-order events (update before scheduled)
                        if azevent_id != azevent_dict["event_id"]:
                            print_warning(
                                f"{self.name}: Out of order az event - "
                                f"tracking {azevent_dict['event_id']}, "
                                f"received update for {azevent_id}"
                            )
                            print_debug(f"Current Event details: {azevent_dict}")
                            print_debug(f"Full current EMS details: {emsevent.model_dump()}")

                            # Preserve timing data from "Unknown" event before resetting
                            timing_data: dict[str, Any] = {}
                            if azevent_dict["event_id"] == "Unknown":
                                # Copy all timing fields (exclude event_id)
                                timing_data = {
                                    k: v for k, v in azevent_dict.items() if k != "event_id"
                                }
                            else:
                                # Save current event with real ID
                                self._add_azmaint(azevent_dict)

                            # Also merge any pending timing data for this node
                            # (from callhome.reboot.giveback with Unknown event_id)
                            if node in self.pending_timing:
                                print_debug(
                                    f"{self.name}: Merging pending timing data "
                                    f"for node {node}: {self.pending_timing[node]}"
                                )
                                for k, v in self.pending_timing[node].items():
                                    if k not in timing_data:
                                        timing_data[k] = v
                                # Clear pending data for this node
                                del self.pending_timing[node]

                            # Check if this event already exists in azmaints
                            if azevent_id and azevent_id in self.azmaints:
                                # Update existing event with status and any timing data
                                status_field = f"az_maint_{status}"
                                self.azmaints[azevent_id][status_field] = event_time
                                # Merge preserved timing data (don't overwrite existing)
                                for k, v in timing_data.items():
                                    if k not in self.azmaints[azevent_id]:
                                        self.azmaints[azevent_id][k] = v
                                print_debug(f"Updated event {azevent_id} with {status_field}")
                                # Reset to empty - this event is already tracked
                                azevent_dict = self._empty_azevent()
                            else:
                                # Create new event dict with proper ID
                                # (scheduled event was missing from EMS)
                                azevent_dict = {
                                    "event_id": azevent_id,
                                    "node": node,
                                    "type": event_type,
                                    "cluster": self.name,
                                    f"az_maint_{status}": event_time,
                                }
                                # Merge preserved timing data
                                azevent_dict.update(timing_data)
                                self.current_azevent = azevent_id or ""
                        else:
                            # Normal case - IDs match
                            azevent_dict[f"az_maint_{status}"] = event_time

                        # For non-HA CVO, complete on az_maint_complete
                        if status == "complete" and self.cluster_type == "CVO":
                            self._add_azmaint(azevent_dict)
                            azevent_dict = self._empty_azevent()

                    case "cf.fsm.nfo.startingGracefulShutdown":
                        # Takeover complete
                        azevent_dict["node_takeover_complete"] = event_time

                    case "kern.shutdown":
                        # Node starts rebooting
                        azevent_dict["node_reboot_starts"] = event_time

                    case "mgr.boot.disk_done":
                        # Node finished rebooting
                        azevent_dict["node_reboot_complete"] = event_time

                    case "cf.fsm.takeoverOfPartnerEnabled":
                        # Node ready for giveback
                        azevent_dict["node_ready_for_giveback"] = event_time

                    case "clam.valid.config":
                        # Giveback starts
                        azevent_dict["node_giveback_starts"] = event_time

                    # SMB client impact events
                    case "vifmgr.lifBeingRemoved":
                        # LIF failover starts - track first occurrence only
                        if "lif_failover_start" not in azevent_dict:
                            azevent_dict["lif_failover_start"] = event_time

                    case "vifmgr.lifsuccessfullymoved":
                        # LIF successfully moved - track last occurrence
                        azevent_dict["lif_failover_complete"] = event_time

                    case "Nblade.cifsWitnessFONotify":
                        # CIFS Witness failover notification
                        azevent_dict["cifs_witness_time"] = event_time
                        client_count, _ = self._parse_cifs_witness_info(emsevent.log_message)
                        if client_count is not None:
                            azevent_dict["cifs_witness_clients"] = client_count

                    case "cf.transition.info":
                        # Protocol transition times - extract CIFS ms
                        cifs_ms = self._parse_cifs_transition_ms(emsevent.log_message)
                        if cifs_ms is not None:
                            azevent_dict["cifs_transition_ms"] = cifs_ms

                    case "ha.sfo.giveback.aggrStart":
                        # Aggregate giveback started - track first occurrence only
                        if "aggr_giveback_start" not in azevent_dict:
                            azevent_dict["aggr_giveback_start"] = event_time

                    case "ha.sfo.giveback.aggrDone":
                        # Aggregate giveback completed - track last occurrence
                        azevent_dict["aggr_giveback_complete"] = event_time

                    case "callhome.reboot.giveback":
                        # Event complete - giveback finished (HA completion marker)
                        azevent_dict["node_giveback_complete"] = event_time
                        azevent_id = azevent_dict["event_id"]
                        if azevent_id == "Unknown":
                            # Scheduled event aged out - save timing data for later
                            # when vsa.scheduledEvent.update arrives
                            event_node = emsevent.node.name
                            timing_data = {k: v for k, v in azevent_dict.items() if k != "event_id"}
                            if timing_data:
                                print_debug(
                                    f"{self.name}: Saving pending timing data "
                                    f"for node {event_node}: {timing_data}"
                                )
                                # Merge with existing pending data for this node
                                if event_node in self.pending_timing:
                                    for k, v in timing_data.items():
                                        if k not in self.pending_timing[event_node]:
                                            self.pending_timing[event_node][k] = v
                                else:
                                    self.pending_timing[event_node] = timing_data
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

        except requests.RequestException:
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
