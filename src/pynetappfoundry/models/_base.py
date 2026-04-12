"""Base class and utilities for ONTAP API models.

Provides OntapModel (Pydantic base with extra='allow'), HasUUID protocol,
and OntapUUID validated type.  This module is the canonical home for
model definitions used across the library.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Annotated, ClassVar, Protocol, runtime_checkable

from pydantic import AfterValidator, BaseModel, ConfigDict, PrivateAttr

if TYPE_CHECKING:
    from pynetappfoundry.data.filters import FieldProxy

_UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def _validate_ontap_uuid(v: str) -> str:
    """Validate an ONTAP UUID string.

    Allows empty strings (ONTAP returns ``""`` for optional UUID fields).

    Args:
        v: The string value to validate.

    Returns:
        The validated string.

    Raises:
        ValueError: If the string is non-empty and not a valid UUID format.
    """
    if v and not _UUID_PATTERN.match(v):
        raise ValueError(f"Invalid UUID: {v}")
    return v


OntapUUID = Annotated[str, AfterValidator(_validate_ontap_uuid)]
"""Dedicated type for ONTAP UUID fields.

A plain ``str`` at runtime with Pydantic validation that rejects malformed
UUIDs on model construction.  Empty strings are allowed because ONTAP
returns ``""`` for optional UUID fields.
"""


class _LazyFieldProxyDescriptor:
    """Descriptor that lazily imports and returns a :class:`FieldProxy`.

    Uses a deferred import to break the circular dependency between
    ``models._base`` and ``data.filters`` (the ``data`` package init
    imports ``data.backends`` which depends on ``cache`` which depends
    on ``models``).
    """

    def __get__(self, obj: object, objtype: type | None = None) -> FieldProxy:
        from pynetappfoundry.data.filters import FieldProxy

        return FieldProxy()


class OntapModel(BaseModel):
    """Base class for all ONTAP API models.

    Provides ``model_config = ConfigDict(extra="allow")`` inherited by all
    subclasses, allowing forward-compatible deserialization of new API fields.

    Tracks which dotted-path fields were populated by the
    :class:`pynetappfoundry.data.DataSource` accessor via the
    ``_fetched_fields`` private attribute.  The set is empty for any model
    constructed directly (e.g. by tests or fixtures); only ``DataSource``
    backends populate it.  Use :meth:`was_fetched` to check whether a
    specific field was populated by a fetch.

    The class-level :attr:`F` descriptor provides typed filter-expression
    support.  ``OntapVolume.F.svm.name == "vs1"`` produces an
    :class:`~pynetappfoundry.data.filters.Eq` expression that compiles to
    the same dict shape accepted by ``DataSource.query().filter()``.
    """

    model_config = ConfigDict(extra="allow")

    F: ClassVar[FieldProxy] = _LazyFieldProxyDescriptor()  # type: ignore[assignment]

    _fetched_fields: set[str] = PrivateAttr(default_factory=set)

    def was_fetched(self, path: str) -> bool:
        """Return whether *path* was populated by a DataSource fetch.

        Args:
            path: Dotted attribute path (e.g. ``"space.size"``).

        Returns:
            True if *path* is in the model's ``_fetched_fields`` set.
        """
        return path in self._fetched_fields


@runtime_checkable
class HasUUID(Protocol):
    """Protocol for models that have a uuid field."""

    uuid: str
