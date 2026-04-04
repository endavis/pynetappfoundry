"""Shared fixtures for benchmark tests."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel, Field

from pynetappfoundry.cache._base import CacheModel

# ---------------------------------------------------------------------------
# Lightweight test models (avoid importing real ONTAP models to keep
# benchmark startup fast and isolated from API schema changes)
# ---------------------------------------------------------------------------


class BenchAutosize(CacheModel):
    """Sub-model for autosize settings."""

    mode: str = ""
    grow_threshold: int = 0
    maximum: int = 0
    minimum: int = 0
    shrink_threshold: int = 0


class BenchSvm(CacheModel):
    """Sub-model for SVM reference."""

    name: str = ""
    uuid: str = ""


class BenchAggregate(CacheModel):
    """Sub-model for aggregate reference."""

    name: str = ""
    uuid: str = ""


class BenchSpace(CacheModel):
    """Sub-model for space usage."""

    available: int = 0
    used: int = 0
    size: int = 0
    percent_used: int = 0
    logical_used: int = 0


class BenchVolume(CacheModel):
    """A simplified volume model for benchmarks.

    Has a mix of scalar fields, nested sub-models, and list fields
    to exercise all serialization paths.
    """

    name: str = ""
    uuid: str = ""
    size: int = 0
    state: str = ""
    style: str = ""
    comment: str = ""
    language: str = ""
    access_time_enabled: bool = False
    is_svm_root: bool = False
    snapshot_count: int = 0
    autosize: BenchAutosize = Field(default_factory=BenchAutosize)
    svm: BenchSvm = Field(default_factory=BenchSvm)
    aggregates: list[BenchAggregate] = Field(default_factory=list)
    space: BenchSpace = Field(default_factory=BenchSpace)
    status: list[str] = Field(default_factory=list)
    cluster_name: str = ""


# For query engine benchmarks — plain BaseModel (not CacheModel)
class QEAutosize(BaseModel):
    """Query engine benchmark sub-model."""

    mode: str = ""
    grow_threshold: int = 0
    maximum: int = 0


class QEAggregate(BaseModel):
    """Query engine benchmark sub-model."""

    name: str = ""
    uuid: str = ""


class QEVolume(BaseModel):
    """Query engine benchmark model for filter/SQL tests."""

    name: str = ""
    uuid: str = ""
    size: int = 0
    state: str = ""
    access_time_enabled: bool = False
    comment: str | None = None
    autosize: QEAutosize = Field(default_factory=QEAutosize)
    aggregates: list[QEAggregate] = Field(default_factory=list)
    status: list[str] = Field(default_factory=list)
    score: float = 0.0


# ---------------------------------------------------------------------------
# Data fixtures
# ---------------------------------------------------------------------------


def _make_volume(i: int) -> BenchVolume:
    """Build a populated BenchVolume for index *i*."""
    return BenchVolume(
        name=f"vol_{i:04d}",
        uuid=f"aaaaaaaa-bbbb-cccc-dddd-{i:012d}",
        size=1073741824 * (i % 10 + 1),
        state="online" if i % 5 != 0 else "offline",
        style="flexvol",
        comment=f"benchmark volume {i}",
        language="en_US",
        access_time_enabled=i % 2 == 0,
        is_svm_root=False,
        snapshot_count=i % 50,
        autosize=BenchAutosize(
            mode="grow" if i % 3 == 0 else "grow_shrink",
            grow_threshold=85,
            maximum=1073741824 * 2,
            minimum=1073741824,
            shrink_threshold=50,
        ),
        svm=BenchSvm(name=f"svm_{i % 4}", uuid=f"svm-uuid-{i % 4}"),
        aggregates=[
            BenchAggregate(name=f"aggr{j}", uuid=f"aggr-uuid-{j}") for j in range(i % 3 + 1)
        ],
        space=BenchSpace(
            available=500_000_000,
            used=500_000_000,
            size=1_000_000_000,
            percent_used=50,
            logical_used=600_000_000,
        ),
        status=["online"],
        cluster_name="bench-cluster",
    )


@pytest.fixture
def bench_volumes_10() -> list[BenchVolume]:
    """10 populated volumes."""
    return [_make_volume(i) for i in range(10)]


@pytest.fixture
def bench_volumes_100() -> list[BenchVolume]:
    """100 populated volumes."""
    return [_make_volume(i) for i in range(100)]


@pytest.fixture
def bench_volumes_1000() -> list[BenchVolume]:
    """1000 populated volumes."""
    return [_make_volume(i) for i in range(1000)]


@pytest.fixture
def nested_api_response() -> dict[str, Any]:
    """A deeply nested dict mimicking an ONTAP API response."""
    return {
        "uuid": "aaaaaaaa-bbbb-cccc-dddd-000000000001",
        "name": "vol_test",
        "svm": {"name": "svm_0", "uuid": "svm-uuid-0"},
        "autosize": {
            "mode": "grow",
            "grow_threshold": 85,
            "maximum": 2147483648,
            "minimum": 1073741824,
            "shrink_threshold": 50,
        },
        "space": {
            "available": 500000000,
            "used": 500000000,
            "size": 1000000000,
            "snapshot": {
                "used": 100000,
                "reserve_percent": 5,
                "autodelete_enabled": True,
            },
        },
        "aggregates": [{"name": f"aggr{i}", "uuid": f"aggr-uuid-{i}"} for i in range(3)],
        "cloud": {
            "provider": "AWS",
            "region": "us-east-1",
            "instance": {"type": "m5.xlarge", "id": "i-1234567890abcdef0"},
        },
        "nodes": [
            {
                "name": f"node-{i:02d}",
                "uuid": f"node-uuid-{i}",
                "model": "FAS8200",
                "uptime": 86400 * (i + 1),
                "interfaces": [{"name": f"lif-{j}", "address": f"10.0.{i}.{j}"} for j in range(4)],
            }
            for i in range(4)
        ],
    }
