"""Tests for DII writes through Mutation (#1003), against the real DII mappings."""

from __future__ import annotations

import importlib
import json
import logging
import pkgutil
from pathlib import Path
from typing import Any, ClassVar
from unittest.mock import MagicMock

import pytest

import pynetappfoundry.cache.dii as dii_root
from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping
from pynetappfoundry.clients.dii.api import DIIWriteTokenMissingError
from pynetappfoundry.core.models import RetryConfig
from pynetappfoundry.models.dii.assets.annotations.model import DiiAssetsAnnotation
from pynetappfoundry.models.dii.collector.datasources.model import DiiCollectorDatasource
from pynetappfoundry.query.mutation import Mutation

REPO_ROOT = Path(__file__).resolve().parents[3]
DII_SPEC_PATH = REPO_ROOT / "docs" / "example-config" / "apis" / "dii" / "all.json"
SENTINEL = "SENTINEL-PW-1003"


def _import_dii_mappings() -> None:
    for _, modname, _ in pkgutil.walk_packages(dii_root.__path__, prefix=dii_root.__name__ + "."):
        if modname.endswith(".mapping"):
            importlib.import_module(modname)


_import_dii_mappings()


@pytest.fixture(scope="module")
def dii_spec() -> dict[str, Any]:
    if not DII_SPEC_PATH.exists():
        pytest.skip("DII spec not available")
    spec: dict[str, Any] = json.loads(DII_SPEC_PATH.read_text(encoding="utf-8"))
    return spec


@pytest.fixture
def client(dii_spec: dict[str, Any]) -> MagicMock:
    mock = MagicMock(spec=["call_endpoint", "api_spec", "read_write"])
    mock.read_write = True
    mock.api_spec = dii_spec
    return mock


def _model(name: str) -> type[Any]:
    mapping = model_registry.get_mapping(name)
    assert mapping is not None
    return mapping.model_class


class TestReadWriteGuard:
    def test_read_client_is_refused(self, dii_spec: dict[str, Any]) -> None:
        read_client = MagicMock(spec=["call_endpoint", "api_spec", "read_write"])
        read_client.read_write = False
        read_client.api_spec = dii_spec
        with pytest.raises(DIIWriteTokenMissingError):
            Mutation(DiiAssetsAnnotation, read_client)
        read_client.call_endpoint.assert_not_called()

    def test_client_without_read_write_attribute_is_refused(self) -> None:
        plain = MagicMock(spec=["call_endpoint", "api_spec"])
        with pytest.raises(DIIWriteTokenMissingError):
            Mutation(DiiAssetsAnnotation, plain)

    @pytest.mark.parametrize(
        "name",
        [
            "DiiAssetsAnnotation",
            "DiiAssetsApplication",
            "DiiMonitorsMonitor",
            "DiiMonitorsRule",
            "DiiCollectorDatasource",
        ],
    )
    def test_every_dii_model_is_guarded(self, name: str) -> None:
        plain = MagicMock(spec=["call_endpoint", "api_spec"])
        with pytest.raises(DIIWriteTokenMissingError):
            Mutation(_model(name), plain)


class TestAnnotation:
    def test_create(self, client: MagicMock) -> None:
        client.call_endpoint.return_value = {"name": "owner", "type": "TEXT"}
        result = Mutation(DiiAssetsAnnotation, client).create(
            name="owner", type_="TEXT", description="who owns it"
        )
        args = client.call_endpoint.call_args
        assert args.args == ("/assets/annotations",)
        assert args.kwargs["method"] == "POST"
        assert args.kwargs["body"] == {
            "name": "owner",
            "type": "TEXT",
            "description": "who owns it",
        }
        assert args.kwargs["retry_config"] == RetryConfig(enabled=False)
        assert isinstance(result, DiiAssetsAnnotation)

    def test_update(self, client: MagicMock) -> None:
        client.call_endpoint.return_value = {}
        Mutation(DiiAssetsAnnotation, client).update("42", description="new")
        client.call_endpoint.assert_called_once_with(
            "/assets/annotations/{id}",
            method="PATCH",
            path_params={"id": "42"},
            body={"description": "new"},
        )

    def test_delete(self, client: MagicMock) -> None:
        Mutation(DiiAssetsAnnotation, client).delete("42")
        client.call_endpoint.assert_called_once_with(
            "/assets/annotations/{id}",
            method="DELETE",
            path_params={"id": "42"},
            body=None,
        )


class TestMonitor:
    def test_create_update_delete(self, client: MagicMock) -> None:
        m = Mutation(_model("DiiMonitorsMonitor"), client)
        client.call_endpoint.return_value = {}
        m.create(name="mon")
        assert client.call_endpoint.call_args.args == ("/monitors/monitors",)
        assert client.call_endpoint.call_args.kwargs["method"] == "POST"
        m.update("9", name="mon2")
        client.call_endpoint.assert_called_with(
            "/monitors/monitors/{id}",
            method="PUT",
            path_params={"id": "9"},
            body={"name": "mon2"},
        )
        m.delete("9")
        client.call_endpoint.assert_called_with(
            "/monitors/monitors/{id}",
            method="DELETE",
            path_params={"id": "9"},
            body=None,
        )


class TestDatasource:
    BODY: ClassVar[dict[str, Any]] = {
        "name": "ds1",
        "acquisitionUnit": {"id": 1},
        "config": {
            "dsTypeId": "t",
            "packages": [{"id": "foundation", "attributes": {"password": SENTINEL}}],
        },
    }

    def test_create_passes_body_through(self, client: MagicMock) -> None:
        client.call_endpoint.return_value = {"name": "ds1", "dataSourceId": "7"}
        result = Mutation(DiiCollectorDatasource, client).create(**self.BODY)
        args = client.call_endpoint.call_args
        assert args.args == ("/collector/datasources",)
        assert args.kwargs["method"] == "POST"
        assert args.kwargs["body"] == self.BODY
        assert args.kwargs["retry_config"] == RetryConfig(enabled=False)
        assert isinstance(result, DiiCollectorDatasource)

    def test_update(self, client: MagicMock) -> None:
        client.call_endpoint.return_value = {}
        Mutation(DiiCollectorDatasource, client).update("7", config=self.BODY["config"])
        client.call_endpoint.assert_called_once_with(
            "/collector/datasources/{dataSourceId}",
            method="PATCH",
            path_params={"dataSourceId": "7"},
            body={"config": self.BODY["config"]},
        )

    def test_delete(self, client: MagicMock) -> None:
        Mutation(DiiCollectorDatasource, client).delete("7")
        client.call_endpoint.assert_called_once_with(
            "/collector/datasources/{dataSourceId}",
            method="DELETE",
            path_params={"dataSourceId": "7"},
            body=None,
        )

    def test_debug_logs_body_keys_not_values(
        self, client: MagicMock, caplog: pytest.LogCaptureFixture
    ) -> None:
        client.call_endpoint.return_value = {}
        m = Mutation(DiiCollectorDatasource, client)
        caplog.set_level(logging.DEBUG)
        m.create(**self.BODY)
        m.update("7", config=self.BODY["config"])
        assert SENTINEL not in caplog.text
        assert "config" in caplog.text


@pytest.mark.parametrize(
    ("name", "template", "placeholder", "method"),
    [
        ("DiiAssetsAnnotation", "/assets/annotations/{id}", "id", "PATCH"),
        ("DiiAssetsApplication", "/assets/applications/{id}", "id", "PUT"),
        ("DiiMonitorsMonitor", "/monitors/monitors/{id}", "id", "PUT"),
        ("DiiMonitorsRule", "/monitors/rules/{id}", "id", "PUT"),
        (
            "DiiCollectorDatasource",
            "/collector/datasources/{dataSourceId}",
            "dataSourceId",
            "PATCH",
        ),
    ],
)
def test_item_template_and_update_method(
    client: MagicMock, name: str, template: str, placeholder: str, method: str
) -> None:
    m = Mutation(_model(name), client)
    assert m._item_template() == (template, placeholder)
    assert m._update_method() == method


class TestErrors:
    def test_poll_is_refused_before_any_call(self, client: MagicMock) -> None:
        m = Mutation(DiiAssetsAnnotation, client)
        with pytest.raises(ValueError, match="poll"):
            m.create(poll=True, name="x")
        with pytest.raises(ValueError, match="poll"):
            m.update("1", poll=True, name="x")
        client.call_endpoint.assert_not_called()

    def _synthetic(self, client: MagicMock, paths: dict[str, Any]) -> Mutation:
        mapping = TypeMapping(
            name="DiiSyntheticThing",
            model_class=DiiAssetsAnnotation,
            api_endpoint="/synthetic/things",
            api_type="dii",
            identifier_field="id",
            records_path="",
            fields=(),
        )
        client.api_spec = {"paths": paths}
        m = Mutation(DiiAssetsAnnotation, client)
        m._mapping = mapping
        return m

    def test_no_item_path(self, client: MagicMock) -> None:
        m = self._synthetic(client, {"/synthetic/things": {"post": {}}})
        with pytest.raises(ValueError, match="item path"):
            m.update("1", name="x")
        with pytest.raises(ValueError, match="item path"):
            m.delete("1")
        client.call_endpoint.assert_not_called()

    def test_item_path_without_patch_or_put(self, client: MagicMock) -> None:
        m = self._synthetic(
            client,
            {"/synthetic/things": {"post": {}}, "/synthetic/things/{id}": {"get": {}}},
        )
        with pytest.raises(ValueError, match="neither PATCH nor PUT"):
            m.update("1", name="x")
        client.call_endpoint.assert_not_called()
