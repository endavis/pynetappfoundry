"""DiiAssetsIscsisessionsInitiatordevice type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.iSCSISessions.initiatorDevice.model import (
    DiiAssetsIscsisessionsInitiatordevice,
)

DIIASSETSISCSISESSIONSINITIATORDEVICE_MAPPING = TypeMapping(
    name="DiiAssetsIscsisessionsInitiatordevice",
    model_class=DiiAssetsIscsisessionsInitiatordevice,
    api_endpoint="/assets/iSCSISessions/{id}/initiatorDevice",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="ip",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="self",
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="wwn",
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsIscsisessionsInitiatordevice", DIIASSETSISCSISESSIONSINITIATORDEVICE_MAPPING
)
