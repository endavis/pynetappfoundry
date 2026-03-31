"""Tests for pynetappfoundry.query.job module."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.jobs.model import OntapJob
from pynetappfoundry.query.job import JobError, JobTracker
from pynetappfoundry.query.mutation import Mutation

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


class FakeVolume(BaseModel):
    """Minimal model for mutation integration tests."""

    name: str = ""
    uuid: str = ""


FAKE_FIELDS = (
    FieldMapping(cache_attr="name", api_path="name"),
    FieldMapping(cache_attr="uuid", api_path="uuid"),
)

FAKE_MAPPING = TypeMapping(
    name="FakeVolumeJob",
    model_class=FakeVolume,
    api_endpoint="/storage/volumes?fields=*",
    fields=FAKE_FIELDS,
    id_field="name",
)


@pytest.fixture(autouse=True)
def _register_mappings() -> Any:
    """Register test mappings and ensure OntapJob mapping is available."""
    # Import to ensure OntapJob mapping is registered
    import pynetappfoundry.cache.ontap.cluster.jobs.mapping  # noqa: F401

    model_registry.register_mapping("FakeVolume", FAKE_MAPPING)
    yield
    model_registry._mappings.pop("FakeVolume", None)


@pytest.fixture()
def mock_client() -> MagicMock:
    """Return a mocked APIWrapper."""
    return MagicMock(spec=["call_endpoint"])


def _job_response(state: str, **kwargs: Any) -> dict[str, Any]:
    """Build a minimal job API response dict."""
    resp: dict[str, Any] = {
        "uuid": "11111111-1111-1111-1111-111111111111",
        "state": state,
        "description": "Test job",
        "message": kwargs.get("message", ""),
        "code": kwargs.get("code", 0),
    }
    if "error_message" in kwargs or "error_code" in kwargs:
        resp["error"] = {}
        if "error_message" in kwargs:
            resp["error"]["message"] = kwargs["error_message"]
        if "error_code" in kwargs:
            resp["error"]["code"] = kwargs["error_code"]
    return resp


# ---------------------------------------------------------------------------
# JobError tests
# ---------------------------------------------------------------------------


class TestJobError:
    """Tests for JobError exception."""

    def test_attributes(self) -> None:
        job = OntapJob(
            uuid="22222222-2222-2222-2222-222222222222",
            state="failure",
            error_message="disk full",
            error_code="123456",
        )
        err = JobError(job)
        assert err.job is job
        assert err.message == "disk full"
        assert err.error_code == "123456"
        assert "22222222-2222-2222-2222-222222222222" in str(err)
        assert "disk full" in str(err)

    def test_falls_back_to_message_field(self) -> None:
        job = OntapJob(
            uuid="22222222-2222-2222-2222-222222222222", state="failure", message="fallback msg"
        )
        err = JobError(job)
        assert err.message == "fallback msg"


# ---------------------------------------------------------------------------
# JobTracker.poll tests
# ---------------------------------------------------------------------------


class TestPoll:
    """Tests for JobTracker.poll."""

    def test_poll_fetches_job(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = _job_response("running")
        tracker = JobTracker("11111111-1111-1111-1111-111111111111", mock_client)
        job = tracker.poll()

        mock_client.call_endpoint.assert_called_once_with(
            "/cluster/jobs/11111111-1111-1111-1111-111111111111"
        )
        assert isinstance(job, OntapJob)
        assert job.state == "running"
        assert job.uuid == "11111111-1111-1111-1111-111111111111"

    def test_poll_updates_last_job(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = _job_response("success")
        tracker = JobTracker("11111111-1111-1111-1111-111111111111", mock_client)
        assert tracker.job is None
        job = tracker.poll()
        assert tracker.job is job


# ---------------------------------------------------------------------------
# JobTracker.wait tests
# ---------------------------------------------------------------------------


class TestWait:
    """Tests for JobTracker.wait."""

    @patch("pynetappfoundry.query.job.time")
    def test_wait_polls_until_success(self, mock_time: MagicMock, mock_client: MagicMock) -> None:
        mock_time.monotonic.side_effect = [0, 1, 2, 3]
        mock_time.sleep = MagicMock()
        mock_client.call_endpoint.side_effect = [
            _job_response("running"),
            _job_response("running"),
            _job_response("success"),
        ]
        tracker = JobTracker(
            "11111111-1111-1111-1111-111111111111", mock_client, poll_interval=1, poll_timeout=10
        )
        job = tracker.wait()

        assert job.state == "success"
        assert mock_client.call_endpoint.call_count == 3
        assert mock_time.sleep.call_count == 2

    @patch("pynetappfoundry.query.job.time")
    def test_wait_raises_on_failure(self, mock_time: MagicMock, mock_client: MagicMock) -> None:
        mock_time.monotonic.side_effect = [0, 1]
        mock_time.sleep = MagicMock()
        mock_client.call_endpoint.side_effect = [
            _job_response("running"),
            _job_response(
                "failure",
                error_message="volume offline",
                error_code="42",
            ),
        ]
        tracker = JobTracker(
            "11111111-1111-1111-1111-111111111111", mock_client, poll_interval=1, poll_timeout=10
        )

        with pytest.raises(JobError, match="volume offline") as exc_info:
            tracker.wait()
        assert exc_info.value.error_code == "42"

    @patch("pynetappfoundry.query.job.time")
    def test_wait_timeout(self, mock_time: MagicMock, mock_client: MagicMock) -> None:
        # monotonic: start=0, after first poll check=100 (exceeds timeout)
        mock_time.monotonic.side_effect = [0, 100]
        mock_time.sleep = MagicMock()
        mock_client.call_endpoint.return_value = _job_response("running")
        tracker = JobTracker(
            "11111111-1111-1111-1111-111111111111", mock_client, poll_interval=1, poll_timeout=5
        )

        with pytest.raises(TimeoutError, match="did not complete"):
            tracker.wait()


# ---------------------------------------------------------------------------
# JobTracker.is_complete tests
# ---------------------------------------------------------------------------


class TestIsComplete:
    """Tests for JobTracker.is_complete property."""

    def test_before_poll(self, mock_client: MagicMock) -> None:
        tracker = JobTracker("11111111-1111-1111-1111-111111111111", mock_client)
        assert tracker.is_complete is False

    def test_terminal_success(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = _job_response("success")
        tracker = JobTracker("11111111-1111-1111-1111-111111111111", mock_client)
        tracker.poll()
        assert tracker.is_complete is True

    def test_terminal_failure(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = _job_response("failure")
        tracker = JobTracker("11111111-1111-1111-1111-111111111111", mock_client)
        tracker.poll()
        assert tracker.is_complete is True

    @pytest.mark.parametrize("state", ["queued", "running", "paused"])
    def test_non_terminal(self, state: str, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = _job_response(state)
        tracker = JobTracker("11111111-1111-1111-1111-111111111111", mock_client)
        tracker.poll()
        assert tracker.is_complete is False


# ---------------------------------------------------------------------------
# JobTracker.from_response tests
# ---------------------------------------------------------------------------


class TestFromResponse:
    """Tests for JobTracker.from_response."""

    def test_extracts_uuid(self, mock_client: MagicMock) -> None:
        response = {"job": {"uuid": "33333333-3333-3333-3333-333333333333"}}
        tracker = JobTracker.from_response(response, mock_client)
        assert tracker._uuid == "33333333-3333-3333-3333-333333333333"

    def test_passes_kwargs(self, mock_client: MagicMock) -> None:
        response = {"job": {"uuid": "33333333-3333-3333-3333-333333333333"}}
        tracker = JobTracker.from_response(response, mock_client, poll_interval=2, poll_timeout=60)
        assert tracker._poll_interval == 2
        assert tracker._poll_timeout == 60

    def test_invalid_response_no_job(self, mock_client: MagicMock) -> None:
        with pytest.raises(ValueError, match="does not contain a job UUID"):
            JobTracker.from_response({}, mock_client)

    def test_invalid_response_no_uuid(self, mock_client: MagicMock) -> None:
        with pytest.raises(ValueError, match="does not contain a job UUID"):
            JobTracker.from_response({"job": {}}, mock_client)

    def test_invalid_response_none(self, mock_client: MagicMock) -> None:
        with pytest.raises(ValueError, match="does not contain a job UUID"):
            JobTracker.from_response(None, mock_client)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Mutation integration tests
# ---------------------------------------------------------------------------


class TestMutationWithPoll:
    """Tests for Mutation.create/update with poll=True."""

    @patch("pynetappfoundry.query.job.time")
    def test_create_with_poll(self, mock_time: MagicMock, mock_client: MagicMock) -> None:
        mock_time.monotonic.side_effect = [0, 1]
        mock_time.sleep = MagicMock()
        mock_client.call_endpoint.side_effect = [
            {"job": {"uuid": "44444444-4444-4444-4444-444444444444"}},
            _job_response("success"),
        ]
        m = Mutation(FakeVolume, mock_client)
        result = m.create(poll=True, name="vol1")
        assert isinstance(result, OntapJob)
        assert result.state == "success"
        assert mock_client.call_endpoint.call_count == 2

    def test_create_without_poll(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "job": {"uuid": "44444444-4444-4444-4444-444444444444"},
        }
        m = Mutation(FakeVolume, mock_client)
        result = m.create(name="vol1")
        assert result == {"job": {"uuid": "44444444-4444-4444-4444-444444444444"}}

    @patch("pynetappfoundry.query.job.time")
    def test_update_with_poll(self, mock_time: MagicMock, mock_client: MagicMock) -> None:
        mock_time.monotonic.side_effect = [0, 1]
        mock_time.sleep = MagicMock()
        mock_client.call_endpoint.side_effect = [
            {"job": {"uuid": "55555555-5555-5555-5555-555555555555"}},
            _job_response("success"),
        ]
        m = Mutation(FakeVolume, mock_client)
        result = m.update(
            "66666666-6666-6666-6666-666666666666",
            poll=True,
            name="vol2",
        )
        assert isinstance(result, OntapJob)
        assert result.state == "success"

    def test_create_with_poll_no_job_in_response(self, mock_client: MagicMock) -> None:
        """When poll=True but response has no job, parse normally."""
        mock_client.call_endpoint.return_value = {
            "name": "vol1",
            "uuid": "abc",
        }
        m = Mutation(FakeVolume, mock_client)
        result = m.create(poll=True, name="vol1")
        assert isinstance(result, FakeVolume)
        assert result.name == "vol1"
