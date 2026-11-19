"""Tests for the Digital Advisor models (placeholder data only)."""

from __future__ import annotations

from pydantic import BaseModel

from pynetappfoundry.data.digitaladvisor_backend import PERSONAL_DATA_FIELDS, _model_of
from pynetappfoundry.models.digitaladvisor import (
    DigitalAdvisorCluster,
    DigitalAdvisorSystem,
    DigitalAdvisorVolume,
)
from pynetappfoundry.models.digitaladvisor.system import DigitalAdvisorSite


def _walk(model: type[BaseModel]) -> set[str]:
    """Return every field name of *model* and of its nested models."""
    names: set[str] = set()
    for name, info in model.model_fields.items():
        names.add(name)
        nested = _model_of(info.annotation)
        if nested is not None:
            names |= _walk(nested)
    return names


def test_no_personal_data_field_in_any_model() -> None:
    for model in (DigitalAdvisorCluster, DigitalAdvisorSystem, DigitalAdvisorVolume):
        assert not _walk(model) & PERSONAL_DATA_FIELDS, model.__name__


def test_site_has_no_address_fields() -> None:
    assert "streetAddress" not in DigitalAdvisorSite.model_fields
    assert "postalCode" not in DigitalAdvisorSite.model_fields


def test_system_parses_nested_objects_and_nulls() -> None:
    system = DigitalAdvisorSystem.model_validate(
        {
            "serialNumber": "SN-1",
            "hostName": None,
            "supportAddOns": ["Protect"],
            "site": {"id": "s1", "city": "Placeholder City"},
            "contract": {"isContractActive": True, "expiryDate": "2030-01-01"},
            "unknownKey": 5,
        }
    )
    assert system.serialNumber == "SN-1"
    assert system.hostName is None
    assert system.site is not None
    assert system.site.city == "Placeholder City"
    assert system.site.name is None
    assert system.contract is not None
    assert system.contract.isContractActive is True
    assert system.contract.expiryDate == "2030-01-01"
    assert system.supportAddOns == ["Protect"]
    assert system.model_extra == {"unknownKey": 5}


def test_volume_float_from_json_int_and_datetime_stays_str() -> None:
    volume = DigitalAdvisorVolume.model_validate(
        {
            "id": "vol-1",
            "snapshotCount": 3,
            "capacity": {"sizeKB": 10, "reportedOn": "2026-01-01T00:00:00Z"},
            "system": {"serialNumber": "SN-1"},
        }
    )
    assert volume.snapshotCount == 3.0
    assert isinstance(volume.snapshotCount, float)
    assert volume.capacity is not None
    assert volume.capacity.reportedOn == "2026-01-01T00:00:00Z"
    assert volume.system is not None
    assert volume.system.serialNumber == "SN-1"


def test_cluster_counts_accept_int_and_float() -> None:
    cluster = DigitalAdvisorCluster.model_validate(
        {
            "id": "c1",
            "storageVirtualMachines": {"totalCount": 2.0},
            "s3Buckets": {"totalCount": 4},
            "capacity": {"lastAsupId": "a1"},
        }
    )
    assert cluster.storageVirtualMachines is not None
    assert cluster.storageVirtualMachines.totalCount == 2
    assert cluster.s3Buckets is not None
    assert cluster.s3Buckets.totalCount == 4
    assert cluster.snapMirrorRelationships is None
