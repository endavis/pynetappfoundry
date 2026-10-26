"""SVM web services -- private CLI: vserver services web show.

Hand-written: the ONTAP REST spec does not describe ``/api/private/cli``
endpoints, so codegen never writes here (#866).
"""

from __future__ import annotations

from typing import Self

from pydantic import model_validator

from pynetappfoundry.models._base import OntapModel


class OntapSvmWebService(OntapModel):
    """One web service on one SVM, from ``vserver services web show``.

    Each SVM has one record per service (``sysmgr``, ``saml``, ...).
    """

    vserver: str = ""
    name: str = ""
    enabled: bool = False
    # ``name`` alone repeats on every SVM, so ``nf cache diff`` keys these
    # records on ``vserver/name``. Always derived; never read from the API.
    service_key: str = ""

    @model_validator(mode="after")
    def _derive_service_key(self) -> Self:
        self.service_key = f"{self.vserver}/{self.name}"
        return self
