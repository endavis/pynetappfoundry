"""Tests for the lazy (PEP 562) exports of ``pynetappfoundry.cache`` (#960)."""

from __future__ import annotations

import importlib

import pytest

import pynetappfoundry.cache as cache_pkg


@pytest.mark.parametrize("name", sorted(cache_pkg.__all__))
def test_every_export_resolves_to_its_defining_object(name: str) -> None:
    module_name = cache_pkg._LAZY_EXPORTS[name]
    expected = getattr(importlib.import_module(module_name), name)
    assert getattr(cache_pkg, name) is expected


def test_lazy_exports_cover_all() -> None:
    assert set(cache_pkg._LAZY_EXPORTS) == set(cache_pkg.__all__)


def test_known_exports_are_the_same_objects_as_in_defining_modules() -> None:
    from pynetappfoundry.cache import collector, db

    assert cache_pkg.ClusterMetadataDB is db.ClusterMetadataDB
    assert cache_pkg.CollectionPhase is collector.CollectionPhase


def test_unknown_attribute_raises_attribute_error() -> None:
    with pytest.raises(AttributeError, match="has no attribute 'nope'"):
        getattr(cache_pkg, "nope")  # noqa: B009  # dynamic name is the point of the test


def test_dir_lists_all_exports() -> None:
    assert set(cache_pkg.__all__) <= set(dir(cache_pkg))


def test_star_import_binds_every_export() -> None:
    namespace: dict[str, object] = {}
    # A star import is only legal at module scope, hence exec.
    exec("from pynetappfoundry.cache import *", namespace)
    assert set(cache_pkg.__all__) <= set(namespace)
