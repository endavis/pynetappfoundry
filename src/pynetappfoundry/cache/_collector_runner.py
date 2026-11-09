"""Phase and task runners for the metadata collector (#899).

Two layers of concurrency live here:

* :class:`PhaseRunner` runs the nine collection phases, either one after the
  other (:class:`SequentialPhaseExecutor`) or on a thread pool
  (:class:`ThreadPoolPhaseExecutor`).  Success and failure bookkeeping is
  shared; only the scheduling and the failure policy differ.
* :func:`run_tasks` runs the per-model fetches inside one composite phase
  (network, storage, relationships, protocols) in parallel or in order.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any

from pynetappfoundry.cache._collector_base import logger
from pynetappfoundry.cache._collector_progress import CollectionPhase

DEFAULT_MAX_WORKERS = 8
NETWORK_FETCH_WORKERS = 5
STORAGE_FETCH_WORKERS = 12
RELATIONSHIPS_FETCH_WORKERS = 3
PROTOCOLS_FETCH_WORKERS = 5

PhaseTask = tuple[CollectionPhase, Callable[[], Any]]


class CollectionError(Exception):
    """Error during metadata collection."""

    pass


def run_tasks(
    tasks: Sequence[tuple[str, Callable[[], Any]]],
    *,
    parallel: bool,
    max_workers: int,
) -> dict[str, Any]:
    """Run keyed tasks and return ``{key: result}``.

    In parallel mode the tasks run on a ``ThreadPoolExecutor`` and the first
    exception raised (in completion order) propagates.  Otherwise they run in
    order on the calling thread.
    """
    results: dict[str, Any] = {}
    if parallel:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(fn): key for key, fn in tasks}
            for future in as_completed(futures):
                results[futures[future]] = future.result()
    else:
        for key, fn in tasks:
            results[key] = fn()
    return results


def run_phase_safe(
    phase: CollectionPhase, collect_method: Callable[[], Any], log_prefix: str
) -> tuple[Any, Exception | None]:
    """Run a collection phase, returning ``(result, error)`` (error is None on success)."""
    try:
        return collect_method(), None
    except Exception as e:
        logger.debug("%s Phase %s failed: %s", log_prefix, phase.value, e)
        return None, e


@dataclass
class PhaseOutcome:
    """The outcome of one phase, with the time it took."""

    phase: CollectionPhase
    result: Any
    error: Exception | None
    elapsed: float


class SequentialPhaseExecutor:
    """Run phases one at a time, lazily, so a caller can stop after a failure."""

    def execute(
        self,
        phases: Sequence[PhaseTask],
        on_start: Callable[[CollectionPhase], None],
        log_prefix: str,
    ) -> Iterator[PhaseOutcome]:
        for phase, method in phases:
            start = time.monotonic()
            on_start(phase)
            logger.debug("%s Collecting %s", log_prefix, phase.value)
            result, error = _call(method)
            yield PhaseOutcome(phase, result, error, time.monotonic() - start)


def _call(method: Callable[[], Any]) -> tuple[Any, Exception | None]:
    try:
        return method(), None
    except Exception as e:
        return None, e


class ThreadPoolPhaseExecutor:
    """Run phases on a thread pool, yielding outcomes as they complete.

    ``on_start`` is not called: the caller announces every phase up front.
    """

    def __init__(self, max_workers: int) -> None:
        self.max_workers = max_workers

    def execute(
        self,
        phases: Sequence[PhaseTask],
        on_start: Callable[[CollectionPhase], None],
        log_prefix: str,
    ) -> Iterator[PhaseOutcome]:
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_phase: dict[
                Future[tuple[Any, Exception | None]], tuple[CollectionPhase, float]
            ] = {}
            for phase, method in phases:
                start = time.monotonic()
                future = executor.submit(run_phase_safe, phase, method, log_prefix)
                future_to_phase[future] = (phase, start)
            for future in as_completed(future_to_phase):
                phase, start = future_to_phase[future]
                elapsed = time.monotonic() - start
                result, error = future.result()
                yield PhaseOutcome(phase, result, error, elapsed)


class PhaseRunner:
    """Run the collection phases and do the progress and log bookkeeping."""

    def __init__(
        self,
        *,
        report: Callable[..., None],
        determine_source: Callable[[CollectionPhase], str | None],
        log_prefix: str,
    ) -> None:
        self._report = report
        self._determine_source = determine_source
        self._log_prefix = log_prefix

    def _on_success(
        self, phase: CollectionPhase, result: Any, elapsed: float, results: dict[str, Any]
    ) -> None:
        source = self._determine_source(phase)
        results[phase.value] = result
        self._report(phase, "completed", elapsed, source=source)
        logger.debug(
            "%s Collected %s in %.2fs via %s",
            self._log_prefix,
            phase.value,
            elapsed,
            source or "unknown",
        )

    def _on_failure(self, phase: CollectionPhase, error: Exception, elapsed: float) -> None:
        self._report(phase, "failed", elapsed, error=str(error))

    def run_sequential(self, phases: Sequence[PhaseTask]) -> dict[str, Any]:
        """Run *phases* in order; the first failure is logged and re-raised unchanged."""
        results: dict[str, Any] = {}
        executor = SequentialPhaseExecutor()
        for outcome in executor.execute(
            phases, lambda p: self._report(p, "starting"), self._log_prefix
        ):
            if outcome.error is None:
                self._on_success(outcome.phase, outcome.result, outcome.elapsed, results)
                continue
            error = outcome.error
            self._on_failure(outcome.phase, error, outcome.elapsed)
            logger.error(
                "%s COLLECTION_ABORTED: Failed phase: %s - %s: %s",
                self._log_prefix,
                outcome.phase.value,
                type(error).__name__,
                str(error),
            )
            raise error
        return results

    def run_parallel(
        self,
        phases: Sequence[PhaseTask],
        cloud: PhaseTask,
        *,
        max_workers: int,
        start_background: Callable[[], None],
    ) -> dict[str, Any]:
        """Run *phases* on a pool, then *cloud* on the calling thread.

        Every phase, including cloud, is announced as starting up front.  A
        failed pool phase is collected; once the pool drains the first error
        is raised as :class:`CollectionError`.  A cloud failure is non-fatal.
        """
        results: dict[str, Any] = {}
        for phase, _ in phases:
            self._report(phase, "starting")
        self._report(cloud[0], "starting")
        start_background()

        errors: list[tuple[CollectionPhase, Exception]] = []
        for outcome in ThreadPoolPhaseExecutor(max_workers).execute(
            phases, lambda p: None, self._log_prefix
        ):
            if outcome.error is None:
                self._on_success(outcome.phase, outcome.result, outcome.elapsed, results)
            else:
                self._on_failure(outcome.phase, outcome.error, outcome.elapsed)
                logger.error(
                    "%s Failed to collect %s: %s",
                    self._log_prefix,
                    outcome.phase.value,
                    outcome.error,
                )
                errors.append((outcome.phase, outcome.error))

        if errors:
            first_phase, first_error = errors[0]
            logger.error(
                "%s COLLECTION_ABORTED: Failed phase: %s - %s: %s",
                self._log_prefix,
                first_phase.value,
                type(first_error).__name__,
                first_error,
            )
            raise CollectionError(
                f"Collection failed for phase {first_phase.value}: {first_error}"
            ) from first_error

        # CLOUD runs after the pool so the nodes are cached for CVO detection.
        # Cloud failures are non-fatal: warn and continue with no cloud data.
        cloud_phase, cloud_method = cloud
        cloud_start = time.monotonic()
        cloud_result, cloud_error = run_phase_safe(cloud_phase, cloud_method, self._log_prefix)
        cloud_elapsed = time.monotonic() - cloud_start
        if cloud_error is None:
            self._on_success(cloud_phase, cloud_result, cloud_elapsed, results)
        else:
            self._on_failure(cloud_phase, cloud_error, cloud_elapsed)
            logger.warning(
                "%s Cloud metadata collection failed (non-fatal): %s",
                self._log_prefix,
                cloud_error,
            )
            results[cloud_phase.value] = []
        return results
