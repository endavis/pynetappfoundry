"""Tests for the Digital Advisor client-side rate limiter (#1051)."""

from __future__ import annotations

from unittest.mock import MagicMock

from pynetappfoundry.clients.digitaladvisor.api import DigitalAdvisorAPIClient, RateLimiter
from pynetappfoundry.clients.digitaladvisor.auth import StaticTokenProvider
from pynetappfoundry.core.models import DigitalAdvisorAPISettings
from tests.unit.clients.digitaladvisor.helpers import FakeClock, gql, session_with


def test_requests_inside_the_window_do_not_sleep() -> None:
    clock = FakeClock()
    limiter = RateLimiter(3, 10.0, clock, clock.sleep)
    for _ in range(3):
        limiter.acquire()
    assert clock.sleeps == []


def test_request_over_the_limit_waits_for_the_oldest_to_leave() -> None:
    clock = FakeClock()
    limiter = RateLimiter(3, 10.0, clock, clock.sleep)
    for _ in range(3):
        limiter.acquire()
        clock.now += 1.0  # stamps at 1000, 1001, 1002; now 1003
    limiter.acquire()
    assert clock.sleeps == [7.0]  # until 1010


def test_client_acquires_once_per_graphql_post_only() -> None:
    limiter = MagicMock(spec=RateLimiter)
    session = session_with(gql({"a": 1}), gql({"a": 2}))
    client = DigitalAdvisorAPIClient(
        settings=DigitalAdvisorAPISettings(personal_access_token="placeholder-pat"),  # type: ignore[arg-type]
        token_provider=StaticTokenProvider("placeholder-pat"),
        session=session,
        rate_limiter=limiter,
    )
    client.query("query { a }")
    client.query("query { a }")
    assert limiter.acquire.call_count == 2
