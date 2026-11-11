"""OntapIgroupInitiator type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.igroups.initiators.model import (
    OntapIgroupInitiator,
    OntapIgroupInitiatorConnectivityTrackingConnection,
    OntapIgroupInitiatorProximityPeerSvm,
    OntapIgroupInitiatorRecord,
)

ONTAPIGROUPINITIATOR_MAPPING = TypeMapping(
    name="OntapIgroupInitiator",
    model_class=OntapIgroupInitiator,
    api_endpoint="/protocols/san/igroups/{igroup.uuid}/initiators?fields=*",
    api_type="ontap",
    parent_mapping="OntapIgroup",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="connectivity_tracking.alerts",
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_tracking.connection_state",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_tracking.connections",
            item_model=OntapIgroupInitiatorConnectivityTrackingConnection,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="igroup.name",
        ),
        FieldMapping(
            cache_attr="igroup.uuid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="proximity.local_svm",
            default=False,
        ),
        FieldMapping(
            cache_attr="proximity.peer_svms",
            item_model=OntapIgroupInitiatorProximityPeerSvm,
            default=[],
        ),
        FieldMapping(
            cache_attr="records",
            item_model=OntapIgroupInitiatorRecord,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapIgroupInitiator", ONTAPIGROUPINITIATOR_MAPPING)
