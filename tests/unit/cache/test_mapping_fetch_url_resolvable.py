"""Guard: no registered ONTAP mapping may fetch a URL with an unfilled placeholder.

A parent fills only the first ``{...}`` placeholder
(``TypeMapping.build_parameterized_url``) and a parentless mapping has every
placeholder stripped (``TypeMapping.build_collection_url``).  A mapping whose
fetch path is wrong because a placeholder went unfilled can never return data.

See: https://github.com/endavis/pynetappfoundry/issues/952
"""

from __future__ import annotations

import importlib
import json
import pkgutil
import re
from pathlib import Path
from typing import ClassVar

import pytest

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping

REPO_ROOT = Path(__file__).resolve().parents[3]
ONTAP_SPEC_PATH = REPO_ROOT / "docs" / "example-config" / "apis" / "ontap" / "openapi3.json"

_PLACEHOLDER = re.compile(r"\{[^}]+\}")

# Mappings known to be unfetchable, each with the issue that resolves it.
_KNOWN_UNRESOLVABLE: dict[str, str] = {
    "OntapExportRule": "#956",
    "OntapEmsFilterRuleResponse": "#932",
}

# Mappings removed because the runtime cannot fill their placeholders (#952).
_DELETED_BY_952: tuple[str, ...] = (
    "OntapApplicationComponentSnapshot",
    "OntapCifsShareAcl",
    "OntapExportClient",
    "OntapFileInfo",
    "OntapKeyManagerKeys",
    "OntapLocalCifsGroupMembers",
    "OntapLunMapReportingNode",
    "OntapPerformanceQtreeMetricResponse",
    "OntapRolePrivilege",
    "OntapS3BucketLifecycleRule",
    "OntapS3BucketSnapshot",
    "OntapUnixGroupUsers",
    "OntapFileDirectorySecurity",
    "OntapSnaplockFileRetention",
    "OntapSnaplockLegalHoldOperation",
    "OntapNdmpPassword",
    "OntapNetgroupFile",
    "OntapLocalCifsUsersAndGroupsImport",
)

_WIRED_BY_952: dict[str, str] = {
    "OntapFpolicyConnection": "OntapFpolicy",
    "OntapFpolicyEngine": "OntapFpolicy",
    "OntapFpolicyEvent": "OntapFpolicy",
    "OntapFpolicyPersistentStore": "OntapFpolicy",
    "OntapFpolicyPolicy": "OntapFpolicy",
    "OntapVscanEvent": "OntapVscan",
    "OntapVscanOnAccess": "OntapVscan",
    "OntapVscanOnDemand": "OntapVscan",
    "OntapVscanScannerPool": "OntapVscan",
}


def _import_all_mapping_modules() -> None:
    import pynetappfoundry.cache.ontap as root

    for _, modname, _ in pkgutil.walk_packages(root.__path__, prefix=root.__name__ + "."):
        if modname.endswith(".mapping"):
            importlib.import_module(modname)


_import_all_mapping_modules()


def _spec_get_paths() -> set[str]:
    # Read the spec directly rather than through tools.codegen: tests under
    # tests/unit/cache are mutmut-selected, and mutmut does not copy tools/ (#873).
    if not ONTAP_SPEC_PATH.exists():
        pytest.skip("ONTAP spec not available")
    paths = json.loads(ONTAP_SPEC_PATH.read_text(encoding="utf-8"))["paths"]
    return {path for path, ops in paths.items() if "get" in ops}


def _unresolved_reason(
    mapping: TypeMapping, spec_get_paths: set[str] | frozenset[str]
) -> str | None:
    """Return why ``mapping`` fetches a wrong URL, or ``None`` when it is fine."""
    path = mapping.api_endpoint.split("?", 1)[0]
    count = len(_PLACEHOLDER.findall(path))
    if count == 0:
        return None
    if mapping.parent_mapping is not None:
        if count != 1:
            return f"{count} placeholders but a parent fills only the first"
        url = mapping.build_parameterized_url("PARENT")
        if _PLACEHOLDER.search(url):
            return f"unfilled placeholder remains in {url}"
        return None
    stripped = mapping.build_collection_url().split("?", 1)[0]
    if count == 1 and path.endswith("}") and stripped in spec_get_paths:
        return None
    return f"stripped path {stripped} is not a spec GET path"


def _ontap_mappings() -> list[tuple[str, TypeMapping]]:
    return [(n, m) for n, m in model_registry.mappings.items() if m.api_type == "ontap"]


class TestRegisteredMappingsAreFetchable:
    def test_every_ontap_mapping_has_a_resolvable_url(self) -> None:
        spec_paths = _spec_get_paths()
        bad = {
            name: reason
            for name, mapping in _ontap_mappings()
            if name not in _KNOWN_UNRESOLVABLE
            and (reason := _unresolved_reason(mapping, spec_paths))
        }
        assert not bad, f"Unfetchable ONTAP mappings: {bad}"

    @pytest.mark.parametrize("name", sorted(_KNOWN_UNRESOLVABLE))
    def test_known_exceptions_are_still_registered_and_still_unresolvable(self, name: str) -> None:
        mapping = model_registry.get_mapping(name)
        assert mapping is not None, f"{name} is gone; remove it from _KNOWN_UNRESOLVABLE"
        assert _unresolved_reason(mapping, _spec_get_paths()) is not None, (
            f"{name} is now fetchable; remove it from _KNOWN_UNRESOLVABLE "
            f"({_KNOWN_UNRESOLVABLE[name]})"
        )

    @pytest.mark.parametrize("name", _DELETED_BY_952)
    def test_deleted_mappings_are_not_registered(self, name: str) -> None:
        assert model_registry.get_mapping(name) is None

    @pytest.mark.parametrize(("name", "parent"), sorted(_WIRED_BY_952.items()))
    def test_wired_children_link_to_parent(self, name: str, parent: str) -> None:
        mapping = model_registry.get_mapping(name)
        assert mapping is not None
        assert mapping.parent_mapping == parent
        assert mapping.parent_id_field == "svm.uuid"


def _synthetic(endpoint: str, parent: str | None) -> TypeMapping:
    from pydantic import BaseModel

    class _Model(BaseModel):
        pass

    return TypeMapping(
        name="Synthetic",
        model_class=_Model,
        api_endpoint=endpoint,
        api_type="ontap",
        parent_mapping=parent,
        parent_id_field="uuid" if parent else None,
        fields=(),
    )


class TestUnresolvedReasonPredicate:
    SPEC: ClassVar[frozenset[str]] = frozenset({"/x", "/svm/svms/{svm.uuid}/web"})

    @pytest.mark.parametrize(
        "endpoint",
        [
            "/a/{x}/b/{y}/c?fields=*",
            "/a/{x}/b?fields=*",
            "/x/{a}/{b}?fields=*",
            "/missing/{id}?fields=*",
        ],
    )
    def test_flagged_without_parent(self, endpoint: str) -> None:
        assert _unresolved_reason(_synthetic(endpoint, None), self.SPEC) is not None

    def test_flagged_two_placeholders_with_parent(self) -> None:
        mapping = _synthetic("/a/{x}/b/{y}/c?fields=*", "Parent")
        assert _unresolved_reason(mapping, self.SPEC) is not None

    def test_passes_single_placeholder_with_parent(self) -> None:
        mapping = _synthetic("/svm/svms/{svm.uuid}/web?fields=*", "Parent")
        assert _unresolved_reason(mapping, self.SPEC) is None

    def test_passes_trailing_placeholder_when_stripped_path_is_a_get(self) -> None:
        assert _unresolved_reason(_synthetic("/x/{id}?fields=*", None), self.SPEC) is None

    def test_passes_without_placeholders(self) -> None:
        assert _unresolved_reason(_synthetic("/x?fields=*", None), self.SPEC) is None
