"""OntapSvmWebService cache model and mapping."""

from pynetappfoundry.cache.ontap.private.cli.vserver.services.web.mapping import (
    ONTAPSVMWEBSERVICE_MAPPING,
)
from pynetappfoundry.models.ontap.private.cli.vserver.services.web.model import OntapSvmWebService

__all__ = ["ONTAPSVMWEBSERVICE_MAPPING", "OntapSvmWebService"]
