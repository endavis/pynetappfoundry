# ADR-0015: Track SMB Client Impact During Azure Maintenance Events

## Status

Accepted

## Decision

Extend the Azure maintenance event tracking (`save-azure` command) to capture **SMB client impact metrics** during CVO HA failover events. Track LIF failover timing, CIFS protocol transition times, CIFS Witness notifications, and aggregate giveback events.

## Rationale

1. **Current tracking is incomplete for SMB impact**: The existing implementation tracks the Azure scheduled event lifecycle (scheduled → started → complete) and HA failover events, but doesn't capture the specific timing of SMB client disruption.

2. **EMS events contain rich SMB impact data**: Analysis of EMS event streams shows that `cf.transition.info` events contain exact CIFS disruption times (in milliseconds), and `Nblade.cifsWitnessFONotify` shows how many Continuously Available clients were notified.

3. **LIF failover is the primary client impact**: When a node fails over, data LIFs must migrate to the partner node. Tracking `vifmgr.lifBeingRemoved` through `vifmgr.lifsuccessfullymoved` captures the exact client disruption window.

4. **Aggregate giveback timing matters**: The `ha.sfo.giveback.aggr*` events show when storage access is impacted during the return phase.

### Events to Track

| Event | Field | Value |
|-------|-------|-------|
| `vifmgr.lifBeingRemoved` | `lif_failover_start` | First LIF removal time |
| `vifmgr.lifsuccessfullymoved` | `lif_failover_complete` | Last LIF migration time |
| `cf.transition.info` | `cifs_transition_ms` | CIFS disruption in ms |
| `Nblade.cifsWitnessFONotify` | `cifs_witness_time`, `cifs_witness_clients` | CA client notification |
| `ha.sfo.giveback.aggrStart` | `aggr_giveback_start` | First aggregate giveback start |
| `ha.sfo.giveback.aggrDone` | `aggr_giveback_complete` | Last aggregate giveback done |

### Analysis Findings

Comparison of three clusters during Azure maintenance showed:
- **ZUSCULTAXCST010**: `cf.transition.info` showed `CIFS=14450ms` (14.4 second disruption)
- **ZUSCULTAXCST011**: `cf.transition.info` showed `CIFS=14709ms` (14.7 second disruption)
- **ZUSCULTAXCST012**: Minimal CIFS events (no CIFS clients connected during maintenance)

These events are consistently available across clusters when CIFS is in use.

## Related Issues

- Issue #92: Azure maintenance event tracking improvements
- PR #106: Fix az_maint_complete when callhome.reboot.giveback comes first

## Related Documentation

- [Azure Maintenance Event Tracking Plan](../plans/azure-smb-impact-tracking.md)
- Source: `src/pynetappfoundry/cli/commands/events/azevents.py`
- Database: `src/pynetappfoundry/db/azevents.py`
