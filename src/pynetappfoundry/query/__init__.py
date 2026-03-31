"""Active query layer for ONTAP models.

Provides :class:`QuerySet` for fluent, type-safe queries against the
ONTAP REST API using existing TypeMapping metadata.
"""

from pynetappfoundry.query.exceptions import MultipleResultsError, NotFoundError
from pynetappfoundry.query.job import JobError, JobTracker
from pynetappfoundry.query.mutation import Mutation
from pynetappfoundry.query.queryset import QuerySet
from pynetappfoundry.query.realtime import (
    compare_realtime,
    fetch_realtime,
    fetch_realtime_collection,
    watch_realtime,
)

__all__ = [
    "JobError",
    "JobTracker",
    "MultipleResultsError",
    "Mutation",
    "NotFoundError",
    "QuerySet",
    "compare_realtime",
    "fetch_realtime",
    "fetch_realtime_collection",
    "watch_realtime",
]
