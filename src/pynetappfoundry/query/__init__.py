"""Active query layer for ONTAP models.

Provides :class:`QuerySet` for fluent, type-safe queries against the
ONTAP REST API using existing TypeMapping metadata.
"""

from pynetappfoundry.query.exceptions import MultipleResultsError, NotFoundError
from pynetappfoundry.query.queryset import QuerySet

__all__ = ["MultipleResultsError", "NotFoundError", "QuerySet"]
