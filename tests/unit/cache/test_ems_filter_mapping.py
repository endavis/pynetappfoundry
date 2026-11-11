"""Regression tests for the filter-shaped OntapEmsFilter mapping (#932)."""

from __future__ import annotations

from pynetappfoundry.cache.field_mapping import parse_api_record
from pynetappfoundry.cache.ontap.support.ems.filters.mapping import ONTAPEMSFILTER_MAPPING
from pynetappfoundry.models.ontap.support.ems.filters.model import (
    OntapEmsFilter,
    OntapEmsFilterRule,
)


def test_parse_filter_record_fills_filter_fields() -> None:
    """A spec-shaped filter record must not collapse to all defaults."""
    record = {
        "name": "f1",
        "system_defined": True,
        "access_control_role": {"name": "admin"},
        "rules": [
            {
                "index": 1,
                "type": "include",
                "message_criteria": {"name_pattern": "wafl.*", "severities": "error"},
                "parameter_criteria": [{"name_pattern": "vol", "value_pattern": "v1"}],
            }
        ],
    }

    result = parse_api_record(ONTAPEMSFILTER_MAPPING, record, "x", skip_realtime=True)

    assert isinstance(result, OntapEmsFilter)
    assert result.name == "f1"
    assert result.system_defined is True
    assert result.access_control_role.name == "admin"
    assert len(result.rules) == 1
    assert isinstance(result.rules[0], OntapEmsFilterRule)
    assert result.rules[0].index == 1
    assert result.rules[0].message_criteria.name_pattern == "wafl.*"
    assert result.rules[0].parameter_criteria[0].value_pattern == "v1"


def test_mapping_is_collection_keyed_by_name() -> None:
    assert ONTAPEMSFILTER_MAPPING.api_endpoint == "/support/ems/filters?fields=*"
    assert ONTAPEMSFILTER_MAPPING.identifier_field == "name"
    assert ONTAPEMSFILTER_MAPPING.records_path == "records"  # the default envelope, not "rules"
