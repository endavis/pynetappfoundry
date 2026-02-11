"""Network LIF information — /network/ip/interfaces."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class NetworkLIF(CacheModel):
    """Network logical interface information."""

    name: str = ""
    ip_address: str = ""
    netmask: str = ""
    home_node: str = ""
    home_port: str = ""
    role: str = ""  # data, cluster, intercluster, management
    svm: str = ""
