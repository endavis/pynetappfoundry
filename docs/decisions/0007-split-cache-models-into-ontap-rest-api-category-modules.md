# ADR-0007: Split cache models into ONTAP REST API category modules

## Status

Accepted

## Decision

Split the monolithic `cache/models.py` (~793 lines, ~35 Pydantic models) into a `cache/models/` package organized by ONTAP REST API URL top-level paths:

- `cloud.py` — `/cloud` API models (CloudMetadata, CloudTargetInfo)
- `cluster.py` — `/cluster` API models (ClusterInfo, NodeInfo, HAInfo, licenses, schedules)
- `name_services.py` — `/name-services` API models (DNSInfo)
- `network.py` — `/network` API models (NetworkLIF, BroadcastDomain, IPSubnetInfo)
- `protocols.py` — `/protocols` API models (export policies, NFS/CIFS/S3, LUNs, igroups)
- `snapmirror.py` — `/snapmirror` API models (SnapMirrorRelationship)
- `storage.py` — `/storage` API models (aggregates, volumes, snapshots, QoS, FlexCache)
- `svm.py` — `/svm` + `/cluster/peers` API models (SVMInfo, ClusterPeer, SVMPeerInfo)
- `base.py` — Schema versioning, HasUUID protocol, container models, CachedClusterMetadata

All existing import paths are preserved via `models/__init__.py` re-exports.

## Rationale

- **Scalability:** 23+ additional ONTAP types are planned for migration to the field mapping framework. Each adds fields and models, making the flat file unsustainable.
- **Navigability:** Organizing by ONTAP REST API URL top-level paths maps directly to ONTAP API documentation, making it intuitive to find and maintain models.
- **No breaking changes:** The `models/__init__.py` re-exports everything, so `from pynetappfoundry.cache.models import X` and `from pynetappfoundry.cache import X` both continue to work unchanged.
- **No circular imports:** Leaf modules have no cross-dependencies or base imports. `base.py` imports from leaf modules directly (safe because leaf modules never import from base).
- **Future extensibility:** Issue #257 proposes deeper URL-tree structure if modules grow large enough.

## Related Issues

- Issue #256: Split cache models.py into ONTAP REST API category modules
- Issue #257: Future deeper URL-tree structure (follow-up)

## Related Documentation

- [Cache Module Reference](../reference/cache.md)
