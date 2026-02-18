"""Re-export network IP cache models from sub-packages."""

from __future__ import annotations

from pynetappfoundry.cache.ontap.network.ip.interfaces import OntapIpInterface
from pynetappfoundry.cache.ontap.network.ip.subnets import OntapIpSubnet

__all__ = [
    "OntapIpInterface",
    "OntapIpSubnet",
]
