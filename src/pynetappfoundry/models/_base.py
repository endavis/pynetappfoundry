"""Base class and utilities for ONTAP API models.

Provides OntapModel (Pydantic base with extra='allow'), HasUUID protocol,
and OntapUUID validated type.  This module is the canonical home for
model definitions used across the library.
"""

from __future__ import annotations

import re
from typing import Annotated, Protocol, runtime_checkable

from pydantic import AfterValidator, BaseModel, ConfigDict, PrivateAttr

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
    """

    model_config = ConfigDict(extra="allow")

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
