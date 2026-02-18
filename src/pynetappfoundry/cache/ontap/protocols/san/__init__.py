"""Re-export SAN cache models from sub-packages."""

from __future__ import annotations

from pynetappfoundry.cache.ontap.protocols.san.igroups import OntapIgroup

__all__ = [
    "OntapIgroup",
]
