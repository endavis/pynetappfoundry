"""Checks behind ``nf doctor`` (ADR-0035).

``nf doctor`` runs three groups of checks and reports each as a
:class:`~pynetappfoundry.core.config_checks.CheckResult` with a fix hint:

* static configuration checks, shared with ``nf config validate`` (ADR-0034);
* :mod:`pynetappfoundry.doctor.environment`: offline checks of ``sops``, the age key,
  SOPS values and the caches;
* :mod:`pynetappfoundry.doctor.live`: read-only requests to each configured API, a GraphQL
  query for Digital Advisor;
* :mod:`pynetappfoundry.doctor.selection`: which rows ``--api`` keeps.

The modules import neither Rich nor click. They sit outside ``core`` because the live
checks use ``clients``, which is the higher layer. This package imports no client or
cache module at import time, so loading it stays cheap.
"""

from __future__ import annotations

API_NAMES: tuple[str, ...] = ("ontap", "aiqum", "dii", "console", "digitaladvisor")
"""The APIs ``nf doctor --api`` accepts."""
