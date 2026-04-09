"""Shared fixtures for ``pynetappfoundry.cache`` unit tests."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache._lazy import LazyClusterMetadata
from pynetappfoundry.core.config import Config


@pytest.fixture
def lazy_metadata_factory() -> Callable[..., LazyClusterMetadata]:
    """Factory that builds :class:`LazyClusterMetadata` with a stub config.

    Forwards all kwargs to ``LazyClusterMetadata(...)`` and defaults
    ``config=`` to a ``MagicMock(spec=Config)`` when the caller doesn't
    supply one. This keeps tests that predate the Phase 3b DataSource
    shim (which added ``config`` as a required kwarg) working without
    each of them having to build a Config.
    """

    def _factory(**kwargs: Any) -> LazyClusterMetadata:
        if "config" not in kwargs:
            kwargs["config"] = MagicMock(spec=Config)
        return LazyClusterMetadata(**kwargs)

    return _factory
