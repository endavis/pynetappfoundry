"""OntapSnmpUser information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSnmpUser(OntapModel):
    """OntapSnmpUser information."""

    authentication_method: str = ""
    comment: str = ""
    engine_id: str = ""
    name: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    scope: str = ""
    snmpv3_authentication_password: str = ""
    snmpv3_authentication_protocol: str = ""
    snmpv3_privacy_password: str = ""
    snmpv3_privacy_protocol: str = ""
    switch_address: str = ""
