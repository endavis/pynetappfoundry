"""Query layer exceptions.

Custom exceptions raised by :class:`~pynetappfoundry.query.queryset.QuerySet`
terminal methods when result cardinality does not match expectations.
"""

from __future__ import annotations

from typing import Any


class NotFoundError(Exception):
    """Raised by :meth:`QuerySet.get` when zero results are returned.

    Attributes:
        model_name: Name of the model that was queried.
        filters: The filter kwargs that produced zero results.
    """

    def __init__(self, model_name: str, filters: dict[str, Any]) -> None:
        self.model_name = model_name
        self.filters = filters
        super().__init__(f"{model_name} matching {filters} does not exist.")


class MultipleResultsError(Exception):
    """Raised by :meth:`QuerySet.get` when more than one result is returned.

    Attributes:
        model_name: Name of the model that was queried.
        count: Number of results returned.
        filters: The filter kwargs that produced multiple results.
    """

    def __init__(self, model_name: str, count: int, filters: dict[str, Any]) -> None:
        self.model_name = model_name
        self.count = count
        self.filters = filters
        super().__init__(
            f"get() returned {count} {model_name} instances, expected 1. Filters: {filters}"
        )
