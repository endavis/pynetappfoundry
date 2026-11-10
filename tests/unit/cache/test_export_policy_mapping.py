"""Regression tests for the OntapExportPolicy policy-shaped mapping (#956)."""

from __future__ import annotations

from pynetappfoundry.cache.field_mapping import parse_api_record
from pynetappfoundry.cache.ontap.protocols.nfs.export_policies.mapping import (
    ONTAPEXPORTPOLICY_MAPPING,
)
from pynetappfoundry.models.ontap.protocols.nfs.export_policies.model import (
    OntapExportPolicy,
)


def test_parse_policy_record_fills_policy_fields() -> None:
    """A spec-shaped policy record must not collapse to all defaults."""
    record = {
        "id": 42,
        "name": "default",
        "svm": {"name": "svm1", "uuid": "u-1"},
        "rules": [
            {
                "index": 1,
                "clients": [{"match": "0.0.0.0/0"}],
                "ro_rule": ["any"],
                "rw_rule": ["none"],
            }
        ],
    }

    policy = parse_api_record(ONTAPEXPORTPOLICY_MAPPING, record, "x", skip_realtime=True)

    assert isinstance(policy, OntapExportPolicy)
    assert policy.id == 42
    assert policy.name == "default"
    assert policy.svm.name == "svm1"
    assert len(policy.rules) == 1
    assert policy.rules[0].index == 1
    assert policy.rules[0].clients[0].match == "0.0.0.0/0"
    assert policy.rules[0].ro_rule == ["any"]


def test_old_rule_shaped_snapshot_still_validates() -> None:
    """Old snapshots carry rule fields at the top level; extra='allow' keeps them loadable."""
    policy = OntapExportPolicy.model_validate({"index": 0, "clients": [], "ro_rule": []})
    assert policy.id == 0
