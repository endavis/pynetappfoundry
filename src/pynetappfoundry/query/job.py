"""Async job tracking for long-running ONTAP operations.

Provides :class:`JobTracker` for polling and waiting on ONTAP jobs
returned by async operations (HTTP 202 responses).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping, parse_api_record
from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.models.ontap.cluster.jobs.model import OntapJob

logger = logging.getLogger(__name__)

_TERMINAL_STATES = frozenset({"success", "failure"})


class JobError(Exception):
    """Raised when an ONTAP job reaches ``failure`` state.

    Attributes:
        job: The failed :class:`OntapJob` instance.
        message: Error message from the job.
        error_code: Error code from the job.
    """

    def __init__(self, job: OntapJob) -> None:
        self.job = job
        self.message = job.error_message or job.message
        self.error_code = job.error_code
        super().__init__(f"Job {job.uuid} failed: {self.message} (code={self.error_code})")


class JobTracker:
    """Track and wait on an ONTAP async job.

    Example::

        tracker = JobTracker.from_response(response, client)
        job = tracker.wait()  # blocks until complete

    Args:
        uuid: Job UUID.
        client: API client for polling.
        poll_interval: Seconds between poll requests.
        poll_timeout: Maximum seconds to wait before raising TimeoutError.
    """

    def __init__(
        self,
        uuid: str,
        client: APIWrapper,
        poll_interval: float = 5,
        poll_timeout: float = 300,
    ) -> None:
        self._uuid = uuid
        self._client = client
        self._poll_interval = poll_interval
        self._poll_timeout = poll_timeout
        self._last_job: OntapJob | None = None

    @property
    def is_complete(self) -> bool:
        """True if the last polled job state is terminal."""
        if self._last_job is None:
            return False
        return self._last_job.state in _TERMINAL_STATES

    @property
    def job(self) -> OntapJob | None:
        """Last polled job instance, or None if never polled."""
        return self._last_job

    def poll(self) -> OntapJob:
        """Fetch current job state with a single GET request.

        Returns:
            Parsed :class:`OntapJob` instance.
        """
        path = f"/cluster/jobs/{self._uuid}"
        logger.debug("JobTracker.poll: GET %s", path)
        response = self._client.call_endpoint(path)
        mapping = self._resolve_mapping()
        job = parse_api_record(mapping, response, f"JobTracker<{self._uuid}>")
        # parse_api_record returns BaseModel; narrow to OntapJob
        self._last_job = job  # type: ignore[assignment]
        return self._last_job  # type: ignore[return-value]

    def wait(self) -> OntapJob:
        """Poll until the job reaches a terminal state.

        Returns:
            The completed :class:`OntapJob` on success.

        Raises:
            JobError: If the job reaches ``failure`` state.
            TimeoutError: If ``poll_timeout`` is exceeded.
        """
        deadline = time.monotonic() + self._poll_timeout
        while True:
            job = self.poll()
            logger.debug("JobTracker.wait: job %s state=%s", self._uuid, job.state)
            if job.state == "success":
                return job
            if job.state == "failure":
                raise JobError(job)
            if time.monotonic() >= deadline:
                msg = (
                    f"Job {self._uuid} did not complete within "
                    f"{self._poll_timeout}s (last state: {job.state})"
                )
                raise TimeoutError(msg)
            time.sleep(self._poll_interval)

    @classmethod
    def from_response(
        cls,
        response: dict[str, Any],
        client: APIWrapper,
        **kwargs: Any,
    ) -> JobTracker:
        """Create a JobTracker from an async API response.

        Args:
            response: API response dict containing ``{"job": {"uuid": "..."}}``.
            client: API client for polling.
            **kwargs: Forwarded to :class:`JobTracker` (e.g. poll_interval).

        Returns:
            New :class:`JobTracker` instance.

        Raises:
            ValueError: If the response does not contain a job UUID.
        """
        try:
            uuid = response["job"]["uuid"]
        except (KeyError, TypeError) as exc:
            msg = f"Response does not contain a job UUID: {response}"
            raise ValueError(msg) from exc
        return cls(uuid=uuid, client=client, **kwargs)

    @staticmethod
    def _resolve_mapping() -> TypeMapping:
        """Look up OntapJob TypeMapping from the registry."""
        mapping = model_registry.get_mapping("OntapJob")
        if mapping is None:  # pragma: no cover
            msg = (
                "No TypeMapping registered for 'OntapJob'. "
                "Ensure the mapping module has been imported."
            )
            raise ValueError(msg)
        return mapping
