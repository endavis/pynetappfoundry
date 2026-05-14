"""Tests for the third-party perf patches applied at project import time."""

from __future__ import annotations

import functools
from typing import Any

import pydantic._internal._fields as _pydantic_fields
import pytest
from pydantic import BaseModel, Field

# Importing the project applies the perf patches; the test file
# exercises them, so the import must run before any assertions touch
# ``_pydantic_fields.takes_validated_data_argument``.
import pynetappfoundry  # noqa: F401


def test_pydantic_takes_validated_data_argument_is_memoized() -> None:
    """The patch in ``pynetappfoundry._perf_patches`` must have wrapped
    Pydantic's ``takes_validated_data_argument`` with a memoization cache."""
    fn = _pydantic_fields.takes_validated_data_argument
    assert isinstance(fn, functools._lru_cache_wrapper), (
        "expected functools.cache wrapper applied at import time; see pynetappfoundry._perf_patches"
    )
    # ``functools.cache`` is ``functools.lru_cache(maxsize=None)``, so
    # the wrapper exposes ``cache_info()`` with ``maxsize is None``.
    info = fn.cache_info()
    assert info.maxsize is None


def test_patched_function_still_returns_correct_results() -> None:
    """The memoized function must agree with Pydantic's documented contract:
    return True iff the factory takes at least one positional argument."""
    fn = _pydantic_fields.takes_validated_data_argument

    def takes_validated_data(validated_data: dict[str, Any]) -> int:
        return len(validated_data)

    def takes_nothing() -> int:
        return 0

    assert fn(takes_validated_data) is True  # type: ignore[arg-type]
    assert fn(takes_nothing) is False  # type: ignore[arg-type]


def test_model_validation_unaffected_by_patch() -> None:
    """End-to-end check: a Pydantic model with default_factory fields
    still validates correctly with the patch in place."""

    class _Inner(BaseModel):
        x: int = 0

    class _Outer(BaseModel):
        name: str
        inner: _Inner = Field(default_factory=_Inner)
        items: list[int] = Field(default_factory=list)

    instance = _Outer.model_validate({"name": "ok"})
    assert instance.name == "ok"
    assert instance.inner.x == 0
    assert instance.items == []


@pytest.mark.parametrize(
    "factory",
    [list, dict, set, str, int, lambda: None],
)
def test_memoization_handles_common_factories(factory: Any) -> None:
    """Cache must accept the kinds of callables Pydantic actually feeds it
    (builtins, lambdas, model classes) without raising ``TypeError``, and
    the cached result must equal the freshly-computed result on second call.
    """
    fn = _pydantic_fields.takes_validated_data_argument
    first = fn(factory)
    second = fn(factory)
    assert first == second
