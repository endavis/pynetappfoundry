"""Compliance guard: deeply nested mapping fields must be tracked.

When a mapping gains (or loses) fields with ``cache_attr`` having 3+ dots
(nesting depth 4+), this test fails so the change is reviewed for
``requires_explicit_fetch`` applicability.  Update ``EXPECTED_COUNTS``
after reviewing the new fields.
"""

from __future__ import annotations

import pynetappfoundry.cache  # noqa: F401 — triggers registry bootstrap
from pynetappfoundry.cache._registry import model_registry

# Baseline counts of fields with cache_attr containing 3+ dots per mapping.
# Update these after reviewing new deeply nested fields for explicit-fetch risk.
EXPECTED_COUNTS: dict[str, int] = {
    "OntapApplication": 34,
    "OntapApplicationTemplate": 34,
    "OntapAudit": 5,
    "OntapBgpPeerGroup": 2,
    "OntapFcInterface": 2,
    "OntapFileInfo": 8,
    "OntapIgroup": 6,
    "OntapIpInterface": 2,
    "OntapLun": 12,
    "OntapNfsService": 66,
    "OntapNodeResponse": 14,
    "OntapNvmeInterface": 4,
    "OntapNvmeService": 44,
    "OntapPort": 7,
    "OntapS3Audit": 5,
    "OntapSnapmirrorTransfer": 6,
    "OntapSoftwareReference": 4,
    "OntapSwitchPort": 5,
    "OntapVolume": 172,
}


def _collect_deeply_nested_counts() -> dict[str, int]:
    """Return mapping-name -> count of fields with 3+ dots in cache_attr."""
    counts: dict[str, int] = {}
    for name, mapping in sorted(model_registry.mappings.items()):
        n = sum(1 for f in mapping.fields if f.cache_attr.count(".") >= 3)
        if n > 0:
            counts[name] = n
    return counts


def test_deeply_nested_field_counts_stable() -> None:
    """Flag new or changed deeply nested fields for review."""
    actual = _collect_deeply_nested_counts()

    # Mappings that gained deeply nested fields (not in baseline).
    new_mappings = set(actual) - set(EXPECTED_COUNTS)
    assert new_mappings == set(), (
        f"New mappings with deeply nested fields (review for requires_explicit_fetch): "
        f"{sorted(new_mappings)}. After reviewing, add them to EXPECTED_COUNTS."
    )

    # Mappings whose count changed.
    changed: dict[str, tuple[int, int]] = {}
    for name, expected in EXPECTED_COUNTS.items():
        actual_count = actual.get(name, 0)
        if actual_count != expected:
            changed[name] = (expected, actual_count)

    assert changed == {}, (
        "Deeply nested field counts changed (review for requires_explicit_fetch):\n"
        + "\n".join(
            f"  {name}: expected {exp}, got {act}" for name, (exp, act) in sorted(changed.items())
        )
        + "\nAfter reviewing, update EXPECTED_COUNTS."
    )
