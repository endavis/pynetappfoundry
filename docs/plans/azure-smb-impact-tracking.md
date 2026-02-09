# Azure Maintenance SMB Client Impact Tracking

## Overview

This plan extends the `save-azure` command to track SMB client impact during Azure maintenance events on CVO HA clusters.

## Background

### Problem Statement

During Azure maintenance events, CVO HA clusters perform failover operations that impact SMB clients. The current implementation tracks:
- Azure scheduled event lifecycle (`vsa.scheduledEvent.*`)
- HA failover events (`cf.fsm.*`, `callhome.reboot.*`)

However, it doesn't capture the specific timing of SMB client disruption, which is critical for:
- Understanding actual client impact duration
- Correlating with SMB client complaints
- Capacity planning for maintenance windows

### Event Timing Analysis

Analysis of three clusters during Azure maintenance revealed:

| Cluster | CIFS Disruption | LIF Failover | Aggregate Giveback |
|---------|-----------------|--------------|-------------------|
| CLUSTER-PROD-01 | 14.4 seconds | 5 LIFs moved | 2 aggregates |
| CLUSTER-PROD-02 | 14.7 seconds | 6 LIFs moved | 4 aggregates |
| CLUSTER-PROD-03 | 1 transition | 2 LIFs moved | 6 aggregates |

CLUSTER-PROD-03 had minimal CIFS activity (no `Nblade.cifsWitnessFONotify` events) because no CIFS clients were connected during maintenance.

---

## Implementation Plan

### Files to Modify

1. **`src/pynetappfoundry/cli/commands/events/azevents.py`**
   - Add new event constants
   - Add new tracking fields
   - Add case handlers in `gather_data()`
   - Add parsing logic for `cf.transition.info` and `Nblade.cifsWitnessFONotify`

2. **`src/pynetappfoundry/db/azevents.py`**
   - Add new columns to the database schema

### New Database Fields

```python
CVO_HA_SMB_FIELDS = [
    "lif_failover_start",        # First vifmgr.lifBeingRemoved time
    "lif_failover_complete",     # Last vifmgr.lifsuccessfullymoved time
    "cifs_transition_ms",        # CIFS disruption in ms from cf.transition.info
    "cifs_witness_time",         # Nblade.cifsWitnessFONotify time
    "cifs_witness_clients",      # Number of CA clients notified
    "aggr_giveback_start",       # First ha.sfo.giveback.aggrStart time
    "aggr_giveback_complete",    # Last ha.sfo.giveback.aggrDone time
]
```

### New Events to Track

```python
SMB_IMPACT_EVENTS = [
    # LIF Events
    "vifmgr.lifBeingRemoved",       # LIF removal starts (impact begins)
    "vifmgr.lifsuccessfullymoved",  # LIF successfully moved (recovery)
    "vifmgr.lifmoved.nodedown",     # LIF moved due to node down
    "vifmgr.lifmoved.byadmin",      # LIF moved by admin (giveback)

    # CIFS Events
    "Nblade.cifsWitnessFONotify",   # CIFS Witness failover notification

    # Protocol Transition Events
    "cf.transition.info",           # Protocol transition times (parse CIFS ms)

    # Aggregate Events
    "ha.sfo.giveback.aggrStart",    # Aggregate giveback started
    "ha.sfo.giveback.aggrDone",     # Aggregate giveback completed
]
```

### Parsing Logic

#### Parse `cf.transition.info`

```python
# Example log message:
# "Takeover Protocol Transition Time(msec):NFS=14450[210|14240]; CIFS=14450[210|14240];"

import re

def parse_cifs_transition(log_message: str) -> int | None:
    """Extract CIFS transition time in milliseconds."""
    match = re.search(r'CIFS=(\d+)\[', log_message)
    if match:
        return int(match.group(1))
    return None
```

#### Parse `Nblade.cifsWitnessFONotify`

```python
# Example log message:
# "The Witness service received a failure notification for the partner node.
#  Notification of 0 CIFS clients to move their Continuously Available
#  connections to this node took 0 milliseconds to complete."

def parse_cifs_witness(log_message: str) -> tuple[int, int]:
    """Extract client count and notification time from CIFS witness event."""
    client_match = re.search(r'Notification of (\d+) CIFS clients', log_message)
    time_match = re.search(r'took (\d+) milliseconds', log_message)

    clients = int(client_match.group(1)) if client_match else 0
    time_ms = int(time_match.group(1)) if time_match else 0

    return clients, time_ms
```

### Event Handling Logic

```python
# In gather_data() switch statement:

case "vifmgr.lifBeingRemoved":
    # Track first LIF removal (start of client impact)
    if "lif_failover_start" not in azevent_dict:
        azevent_dict["lif_failover_start"] = emsevent["time"]

case "vifmgr.lifsuccessfullymoved":
    # Track latest LIF migration (end of client impact)
    azevent_dict["lif_failover_complete"] = emsevent["time"]

case "cf.transition.info":
    # Parse CIFS transition time
    log_message = emsevent["log_message"]
    cifs_ms = parse_cifs_transition(log_message)
    if cifs_ms is not None:
        # Keep the maximum CIFS transition time seen
        current = azevent_dict.get("cifs_transition_ms", 0)
        azevent_dict["cifs_transition_ms"] = max(current, cifs_ms)

case "Nblade.cifsWitnessFONotify":
    # Parse CIFS witness notification
    log_message = emsevent["log_message"]
    clients, time_ms = parse_cifs_witness(log_message)
    azevent_dict["cifs_witness_time"] = emsevent["time"]
    azevent_dict["cifs_witness_clients"] = clients

case "ha.sfo.giveback.aggrStart":
    # Track first aggregate giveback start
    if "aggr_giveback_start" not in azevent_dict:
        azevent_dict["aggr_giveback_start"] = emsevent["time"]

case "ha.sfo.giveback.aggrDone":
    # Track latest aggregate giveback completion
    azevent_dict["aggr_giveback_complete"] = emsevent["time"]
```

---

## Database Schema Changes

Add to `AzEventsDB.create_table()`:

```sql
lif_failover_start TEXT,
lif_failover_complete TEXT,
cifs_transition_ms INTEGER,
cifs_witness_time TEXT,
cifs_witness_clients INTEGER,
aggr_giveback_start TEXT,
aggr_giveback_complete TEXT
```

---

## Verification Plan

1. **Run `doit check`** to ensure all tests pass
2. **Run `save-azure`** on test clusters:
   - CLUSTER-PROD-01 (has CIFS clients)
   - CLUSTER-PROD-02 (has CIFS clients)
   - CLUSTER-PROD-03 (no CIFS clients - verify empty fields)
3. **Query database** to verify new fields are populated:
   ```sql
   SELECT cluster, event_id,
          lif_failover_start, lif_failover_complete,
          cifs_transition_ms, cifs_witness_clients,
          aggr_giveback_start, aggr_giveback_complete
   FROM azure_events
   WHERE cluster LIKE 'CLUSTER-PROD-%';
   ```
4. **Verify CU012** shows NULL for CIFS witness fields (expected - no clients)

---

## Related

- ADR: [0002-track-smb-client-impact-azure-maintenance](../decisions/0002-track-smb-client-impact-azure-maintenance.md)
- Issue: #92 (Azure maintenance event tracking improvements)
- PR: #106 (Fix az_maint_complete timing race condition)
