"""Shared fixtures for pynetappfoundry.data tests.

Provides synthetic Pydantic models, a synthetic TypeMapping covering
all four field strategies, and helpers to register/unregister the
fake mapping in :mod:`pynetappfoundry.cache._registry`.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from tests.unit.data._fakes import FakeComposite, FakeVolume

__all__ = ["FakeComposite", "FakeVolume"]


@pytest.fixture
def fake_volume_mapping() -> Iterator[TypeMapping]:
    """Register a synthetic FakeVolume mapping for the duration of one test."""
    mapping = TypeMapping(
        name="FakeVolume",
        model_class=FakeVolume,
        api_endpoint="/storage/fake-volumes?fields=*",
        api_type="ontap",
        identifier_field="uuid",
        fields=(
            FieldMapping(cache_attr="name", cache_strategy="cache"),
            FieldMapping(cache_attr="uuid", cache_strategy="cache"),
            FieldMapping(cache_attr="size", cache_strategy="cache"),
            FieldMapping(cache_attr="iops", cache_strategy="realtime"),
            FieldMapping(cache_attr="is_root", cache_strategy="derived"),
            FieldMapping(
                cache_attr="files_scanned",
                cache_strategy="cache",
                requires_explicit_fetch=True,
            ),
        ),
    )
    model_registry.register_mapping("FakeVolume", mapping)
    try:
        yield mapping
    finally:
        # Defensive cleanup -- remove from the singleton.
        model_registry._mappings.pop("FakeVolume", None)


@pytest.fixture
def fake_composite_mapping() -> Iterator[TypeMapping]:
    """Register a composite-key mapping for identifier-normalization tests."""
    mapping = TypeMapping(
        name="FakeComposite",
        model_class=FakeComposite,
        api_endpoint="/composite?fields=*",
        api_type="ontap",
        identifier_field=("svm_name", "name"),
        fields=(
            FieldMapping(cache_attr="svm_name", cache_strategy="cache"),
            FieldMapping(cache_attr="name", cache_strategy="cache"),
        ),
    )
    model_registry.register_mapping("FakeComposite", mapping)
    try:
        yield mapping
    finally:
        model_registry._mappings.pop("FakeComposite", None)


@pytest.fixture
def mock_config() -> Any:
    """A bare MagicMock standing in for :class:`Config`."""
    return MagicMock(name="Config")
