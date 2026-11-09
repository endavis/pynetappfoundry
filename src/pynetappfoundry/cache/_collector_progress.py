"""Progress reporting types for the metadata collector (#899)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum


class CollectionPhase(Enum):
    """Phases of metadata collection."""

    CLOUD = "cloud"
    CLUSTER = "cluster"
    NODES = "nodes"
    NETWORK = "network"
    STORAGE = "storage"
    LICENSES = "licenses"
    MEDIATOR = "mediator"
    RELATIONSHIPS = "relationships"
    PROTOCOLS = "protocols"


@dataclass
class ProgressInfo:
    """Progress information for a collection phase."""

    phase: CollectionPhase
    phase_name: str
    status: str  # "starting", "completed", "failed"
    elapsed_seconds: float = 0.0
    error: str | None = None
    source: str | None = None  # "api", "cli", or None


# Type alias for progress callback
ProgressCallback = Callable[[ProgressInfo], None]

# Human-readable names for collection phases
PHASE_NAMES: dict[CollectionPhase, str] = {
    CollectionPhase.CLOUD: "Cloud metadata",
    CollectionPhase.CLUSTER: "Cluster info",
    CollectionPhase.NODES: "Nodes",
    CollectionPhase.NETWORK: "Network",
    CollectionPhase.STORAGE: "Storage",
    CollectionPhase.LICENSES: "Licenses",
    CollectionPhase.MEDIATOR: "Mediator",
    CollectionPhase.RELATIONSHIPS: "Relationships",
    CollectionPhase.PROTOCOLS: "Protocols",
}


def report_progress(
    callback: ProgressCallback | None,
    phase: CollectionPhase,
    status: str,
    elapsed_seconds: float = 0.0,
    error: str | None = None,
    source: str | None = None,
    phase_names: dict[CollectionPhase, str] | None = None,
) -> None:
    """Report progress to *callback* if configured.

    Args:
        callback: Progress callback, or None to do nothing.
        phase: The collection phase.
        status: Status string ("starting", "completed", "failed").
        elapsed_seconds: Time taken for this phase.
        error: Error message if failed.
        source: Data source used ("api", "cli").
        phase_names: Phase display names (defaults to :data:`PHASE_NAMES`).
    """
    if callback:
        names = PHASE_NAMES if phase_names is None else phase_names
        callback(
            ProgressInfo(
                phase=phase,
                phase_name=names.get(phase, phase.value),
                status=status,
                elapsed_seconds=elapsed_seconds,
                error=error,
                source=source,
            )
        )
