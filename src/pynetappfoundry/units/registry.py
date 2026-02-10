"""Unit registry mapping API fields to their units.

The registry is keyed by ``(endpoint, api_field_path)`` tuples, where
``endpoint`` is the base path without query parameters (e.g.,
``"/storage/volumes"``) and ``api_field_path`` is the dot-notation path
within the API response.

Each API type (ONTAP, DII, AIQUM) maintains its own ``UnitRegistry``
instance to avoid endpoint collisions across different APIs.

Example:
    >>> from pynetappfoundry.units.ontap_units import ontap_registry
    >>> entry = ontap_registry.get("/storage/volumes", "size")
    >>> entry.unit.symbol
    'B'
    >>> entry.source
    'ONTAP REST API: field value is in bytes'
"""

from __future__ import annotations

from dataclasses import dataclass

from pynetappfoundry.units.dimensions import Unit


@dataclass(frozen=True)
class UnitEntry:
    """A registry entry mapping an API field to its unit.

    Attributes:
        endpoint: The API endpoint base path (e.g., ``"/storage/volumes"``).
            No query parameters.
        api_field_path: Dot-notation path within the API response
            (e.g., ``"size"``, ``"autosize.maximum"``).
        unit: The Unit instance for this field.
        source: Traceability string documenting where the unit information
            came from.
    """

    endpoint: str
    api_field_path: str
    unit: Unit
    source: str


class UnitRegistry:
    """Registry of unit metadata for API fields.

    Provides lookup by ``(endpoint, api_field_path)`` and bulk registration.
    Each API type (ONTAP, DII, AIQUM) should have its own instance.
    """

    def __init__(self) -> None:
        self._entries: dict[tuple[str, str], UnitEntry] = {}

    def register(self, entry: UnitEntry) -> None:
        """Register a unit entry.

        Args:
            entry: The UnitEntry to register.

        Raises:
            ValueError: If a different entry is already registered for the
                same ``(endpoint, api_field_path)`` key.
        """
        key = (entry.endpoint, entry.api_field_path)
        existing = self._entries.get(key)
        if existing is not None and existing != entry:
            raise ValueError(
                f"Conflicting registration for {key}: "
                f"existing={existing.unit.name}, new={entry.unit.name}"
            )
        self._entries[key] = entry

    def register_many(self, entries: tuple[UnitEntry, ...]) -> None:
        """Register multiple entries at once.

        Args:
            entries: Tuple of UnitEntry instances to register.
        """
        for entry in entries:
            self.register(entry)

    def get(self, endpoint: str, api_field_path: str) -> UnitEntry | None:
        """Look up a unit entry by endpoint and field path.

        Args:
            endpoint: The API endpoint base path.
            api_field_path: The dot-notation field path.

        Returns:
            The UnitEntry if found, None otherwise.
        """
        return self._entries.get((endpoint, api_field_path))

    def get_by_endpoint(self, endpoint: str) -> tuple[UnitEntry, ...]:
        """Get all unit entries for a given endpoint.

        Args:
            endpoint: The API endpoint base path.

        Returns:
            Tuple of matching UnitEntry instances, sorted by api_field_path.
        """
        return tuple(
            sorted(
                (e for e in self._entries.values() if e.endpoint == endpoint),
                key=lambda e: e.api_field_path,
            )
        )

    def all_entries(self) -> tuple[UnitEntry, ...]:
        """Get all registered entries.

        Returns:
            Tuple of all UnitEntry instances, sorted by
            ``(endpoint, api_field_path)``.
        """
        return tuple(
            sorted(
                self._entries.values(),
                key=lambda e: (e.endpoint, e.api_field_path),
            )
        )

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, key: tuple[str, str]) -> bool:
        return key in self._entries
