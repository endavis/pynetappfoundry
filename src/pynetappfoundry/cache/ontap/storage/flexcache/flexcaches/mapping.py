"""OntapFlexcache type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.flexcache.flexcaches.model import (
    OntapFlexcache,
    OntapFlexcacheAggregate,
    OntapFlexcacheOrigin,
)

ONTAPFLEXCACHE_MAPPING = TypeMapping(
    name="OntapFlexcache",
    model_class=OntapFlexcache,
    api_endpoint="/storage/flexcache/flexcaches?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="aggregates",
            item_model=OntapFlexcacheAggregate,
            default=[],
        ),
        FieldMapping(
            cache_attr="atime_scrub.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="atime_scrub.period",
            default=0,
        ),
        FieldMapping(
            cache_attr="cifs_change_notify.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="constituents_per_aggregate",
            default=0,
        ),
        FieldMapping(
            cache_attr="dr_cache",
            default=False,
        ),
        FieldMapping(
            cache_attr="global_file_locking_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="guarantee.type_",
            api_path="guarantee.type",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="origins",
            item_model=OntapFlexcacheOrigin,
            default=[],
        ),
        FieldMapping(
            cache_attr="override_encryption",
            default=False,
        ),
        FieldMapping(
            cache_attr="path",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="prepopulate.dir_paths",
            default=[],
        ),
        FieldMapping(
            cache_attr="prepopulate.exclude_dir_paths",
            default=[],
        ),
        FieldMapping(
            cache_attr="prepopulate.recurse",
            default=False,
        ),
        FieldMapping(
            cache_attr="relative_size.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="relative_size.percentage",
            default=0,
        ),
        FieldMapping(
            cache_attr="size",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="use_tiered_aggregate",
            default=False,
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="writeback.enabled",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapFlexcache", ONTAPFLEXCACHE_MAPPING)
