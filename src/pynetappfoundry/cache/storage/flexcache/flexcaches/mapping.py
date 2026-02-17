"""OntapFlexcache type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.storage.flexcache.flexcaches.model import (
    OntapFlexcache,
    OntapFlexcacheAggregate,
    OntapFlexcacheOrigin,
)


def _transform_aggregates(record: dict[str, Any]) -> list[OntapFlexcacheAggregate]:
    """Transform aggregates into OntapFlexcacheAggregate list."""
    return [OntapFlexcacheAggregate(**item) for item in record.get("aggregates", [])]


def _transform_origins(record: dict[str, Any]) -> list[OntapFlexcacheOrigin]:
    """Transform origins into OntapFlexcacheOrigin list."""
    return [OntapFlexcacheOrigin(**item) for item in record.get("origins", [])]


ONTAPFLEXCACHE_MAPPING = TypeMapping(
    name="OntapFlexcache",
    model_class=OntapFlexcache,
    api_endpoint="/storage/flexcache/flexcaches?fields=*,guarantee,path,size",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="aggregates",
            transform=_transform_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="atime_scrub_enabled",
            api_path="atime_scrub.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="atime_scrub_period",
            api_path="atime_scrub.period",
            default=0,
        ),
        FieldMapping(
            cache_attr="cifs_change_notify_enabled",
            api_path="cifs_change_notify.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="constituents_per_aggregate",
            api_path="constituents_per_aggregate",
            default=0,
        ),
        FieldMapping(
            cache_attr="dr_cache",
            api_path="dr_cache",
            default=False,
        ),
        FieldMapping(
            cache_attr="global_file_locking_enabled",
            api_path="global_file_locking_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="guarantee_type",
            api_path="guarantee.type",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="origins",
            transform=_transform_origins,
            default=[],
        ),
        FieldMapping(
            cache_attr="override_encryption",
            api_path="override_encryption",
            default=False,
        ),
        FieldMapping(
            cache_attr="path",
            api_path="path",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="prepopulate_dir_paths",
            api_path="prepopulate.dir_paths",
            default=[],
        ),
        FieldMapping(
            cache_attr="prepopulate_exclude_dir_paths",
            api_path="prepopulate.exclude_dir_paths",
            default=[],
        ),
        FieldMapping(
            cache_attr="prepopulate_recurse",
            api_path="prepopulate.recurse",
            default=False,
        ),
        FieldMapping(
            cache_attr="relative_size_enabled",
            api_path="relative_size.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="relative_size_percentage",
            api_path="relative_size.percentage",
            default=0,
        ),
        FieldMapping(
            cache_attr="size",
            api_path="size",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="use_tiered_aggregate",
            api_path="use_tiered_aggregate",
            default=False,
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="writeback_enabled",
            api_path="writeback.enabled",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapFlexcache", ONTAPFLEXCACHE_MAPPING)
