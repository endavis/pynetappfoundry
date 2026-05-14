"""Runtime monkey-patches that compensate for known third-party performance gaps.

Each patch in this module:

1. Targets a specific, profiled hot path.
2. Wraps a deterministic function with a memoizing decorator (or equivalent).
3. Is reversible by deleting the corresponding block once the upstream
   library ships an equivalent fix.

This module must be imported **before** any project model is constructed —
``pynetappfoundry/__init__.py`` does that on its first line, and Python
guarantees ``__init__.py`` runs before any submodule import, so importing
any ``pynetappfoundry.*`` module also applies the patches first.

Each patch is idempotent: re-application returns the same wrapped callable.
"""

from __future__ import annotations

import functools

import pydantic._internal._fields as _pydantic_fields


def _patch_pydantic_takes_validated_data_argument() -> None:
    """Memoize ``pydantic._internal._fields.takes_validated_data_argument``.

    The function asks "does this default_factory callable take a
    ``validated_data`` argument?" via ``inspect.signature``. It is called
    once per ``default_factory`` field per model instance during
    ``model_post_init``. For a model with many default_factory fields
    (e.g., ``OntapVolume`` has ~155 such fields), a batch deserialization
    of 500 instances triggers ~123k ``inspect.signature`` calls and burns
    ~16 of 17.6 seconds total wall time (see issue #728 cProfile data).

    The answer is fully determined by the factory callable identity, so a
    plain ``functools.cache`` wrapper is sound: the cached "yes/no"
    result remains correct as long as the factory function doesn't get
    redefined in place — and Pydantic's own model machinery already
    treats factory identity as a key.

    Speedup measured on a 500-volume cache load: ~17,600 ms -> ~650 ms
    per call (~17-25x faster); cache hit rate 99.7%.

    Remove this patch when Pydantic ships a memoized version of the
    function upstream (track via issue #728's linked upstream issue).
    """
    fn = _pydantic_fields.takes_validated_data_argument
    if isinstance(fn, functools._lru_cache_wrapper):  # already patched
        return
    _pydantic_fields.takes_validated_data_argument = functools.cache(fn)  # type: ignore[assignment]


_patch_pydantic_takes_validated_data_argument()
