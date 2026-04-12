"""Tests for pynetappfoundry.data.filters — typed filter DSL."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.field_mapping import TypeMapping
from pynetappfoundry.data.filters import (
    And,
    Eq,
    FieldProxy,
    Ge,
    Gt,
    In,
    IsNull,
    Le,
    Lt,
    Ne,
    Not,
    NotIn,
    compile_filters,
)
from pynetappfoundry.data.source import DataSource

from .conftest import FakeVolume

# ---------------------------------------------------------------------------
# FieldProxy attribute traversal
# ---------------------------------------------------------------------------


class TestFieldProxy:
    def test_single_attr(self) -> None:
        assert FieldProxy().name._path == "name"

    def test_nested_attr(self) -> None:
        assert FieldProxy().svm.name._path == "svm.name"

    def test_deep_nested(self) -> None:
        assert FieldProxy().a.b.c.d._path == "a.b.c.d"

    def test_empty_root_path(self) -> None:
        assert FieldProxy()._path == ""


# ---------------------------------------------------------------------------
# FilterExpression construction via operators
# ---------------------------------------------------------------------------


class TestFilterExpressions:
    def test_eq(self) -> None:
        result = FieldProxy().name == "vol1"
        assert result == Eq("name", "vol1")

    def test_ne(self) -> None:
        result = FieldProxy().name != "vol1"
        assert result == Ne("name", "vol1")

    def test_lt(self) -> None:
        result = FieldProxy().size < 100
        assert result == Lt("size", 100)

    def test_gt(self) -> None:
        result = FieldProxy().size > 100
        assert result == Gt("size", 100)

    def test_le(self) -> None:
        result = FieldProxy().size <= 100
        assert result == Le("size", 100)

    def test_ge(self) -> None:
        result = FieldProxy().size >= 100
        assert result == Ge("size", 100)

    def test_in(self) -> None:
        result = FieldProxy().state.in_(["online", "mixed"])
        assert result == In("state", ("online", "mixed"))

    def test_not_in(self) -> None:
        result = FieldProxy().state.not_in(["offline", "error"])
        assert result == NotIn("state", ("offline", "error"))

    def test_is_null(self) -> None:
        result = FieldProxy().comment.is_null()
        assert result == IsNull("comment")

    def test_invert(self) -> None:
        eq = Eq("name", "vol1")
        result = ~eq
        assert result == Not(Eq("name", "vol1"))

    def test_and(self) -> None:
        a = Eq("a", 1)
        b = Eq("b", 2)
        result = a & b
        assert result == And((Eq("a", 1), Eq("b", 2)))

    def test_field_proxy_hash(self) -> None:
        """FieldProxy overrides __hash__ to use id(self)."""
        fp = FieldProxy()
        assert hash(fp) == id(fp)

    def test_in_stores_tuple(self) -> None:
        """In.values is stored as a tuple for frozen hashability."""
        result = FieldProxy().x.in_([1, 2, 3])
        assert isinstance(result.values, tuple)

    def test_not_in_stores_tuple(self) -> None:
        """NotIn.values is stored as a tuple for frozen hashability."""
        result = FieldProxy().x.not_in([1, 2, 3])
        assert isinstance(result.values, tuple)


# ---------------------------------------------------------------------------
# compile_filters()
# ---------------------------------------------------------------------------


class TestCompileFilters:
    def test_single_eq(self) -> None:
        eq_dict, wheres = compile_filters(Eq("svm.name", "vs1"))
        assert eq_dict == {"svm.name": "vs1"}
        assert wheres == ()

    def test_ne(self) -> None:
        eq_dict, wheres = compile_filters(Ne("state", "offline"))
        assert eq_dict == {}
        assert wheres == ("state != 'offline'",)

    def test_lt(self) -> None:
        _, wheres = compile_filters(Lt("size", 1000))
        assert wheres == ("size < 1000",)

    def test_gt(self) -> None:
        _, wheres = compile_filters(Gt("size", 1000))
        assert wheres == ("size > 1000",)

    def test_le(self) -> None:
        _, wheres = compile_filters(Le("size", 1000))
        assert wheres == ("size <= 1000",)

    def test_ge(self) -> None:
        _, wheres = compile_filters(Ge("size", 1000))
        assert wheres == ("size >= 1000",)

    def test_in(self) -> None:
        _, wheres = compile_filters(In("state", ("online", "mixed")))
        assert wheres == ("state in ('online', 'mixed')",)

    def test_not_in(self) -> None:
        _, wheres = compile_filters(NotIn("state", ("offline", "error")))
        assert wheres == ("state not in ('offline', 'error')",)

    def test_is_null(self) -> None:
        _, wheres = compile_filters(IsNull("comment"))
        assert wheres == ("comment is null",)

    def test_not_eq(self) -> None:
        """Not(Eq(...)) special-cases to ``field != value``."""
        _, wheres = compile_filters(Not(Eq("name", "vol1")))
        assert wheres == ("name != 'vol1'",)

    def test_not_non_eq(self) -> None:
        """Not(non-Eq) wraps in ``not (...)``."""
        _, wheres = compile_filters(Not(Gt("size", 100)))
        assert wheres == ("not (size > 100)",)

    def test_and(self) -> None:
        expr = And((Eq("a", 1), Ne("b", "x")))
        eq_dict, wheres = compile_filters(expr)
        assert eq_dict == {"a": 1}
        assert wheres == ("b != 'x'",)

    def test_mixed_eq_and_non_eq(self) -> None:
        eq_dict, wheres = compile_filters(
            Eq("svm.name", "vs1"),
            Gt("size", 1000),
        )
        assert eq_dict == {"svm.name": "vs1"}
        assert wheres == ("size > 1000",)

    def test_numeric_values_unquoted(self) -> None:
        _, wheres = compile_filters(Gt("size", 1000))
        assert wheres == ("size > 1000",)

    def test_float_values_unquoted(self) -> None:
        _, wheres = compile_filters(Gt("ratio", 0.5))
        assert wheres == ("ratio > 0.5",)

    def test_string_values_quoted(self) -> None:
        _, wheres = compile_filters(Ne("state", "offline"))
        assert wheres == ("state != 'offline'",)

    def test_in_with_numeric_values(self) -> None:
        _, wheres = compile_filters(In("size", (100, 200)))
        assert wheres == ("size in (100, 200)",)

    def test_empty_expressions(self) -> None:
        eq_dict, wheres = compile_filters()
        assert eq_dict == {}
        assert wheres == ()

    def test_multiple_eq_merge(self) -> None:
        eq_dict, wheres = compile_filters(
            Eq("svm.name", "vs1"),
            Eq("state", "online"),
        )
        assert eq_dict == {"svm.name": "vs1", "state": "online"}
        assert wheres == ()


# ---------------------------------------------------------------------------
# OntapModel.F descriptor
# ---------------------------------------------------------------------------


class TestOntapModelF:
    def test_f_descriptor_returns_proxy(self) -> None:
        result = FakeVolume.F
        assert isinstance(result, FieldProxy)

    def test_f_nested_traversal(self) -> None:
        assert FakeVolume.F.svm.name._path == "svm.name"

    def test_f_comparison(self) -> None:
        result = FakeVolume.F.svm.name == "vs1"
        assert isinstance(result, Eq)
        assert result == Eq("svm.name", "vs1")

    def test_f_descriptor_fresh_per_access(self) -> None:
        """Each access to .F returns a new FieldProxy (no stale state)."""
        fp1 = FakeVolume.F
        fp2 = FakeVolume.F
        assert fp1 is not fp2

    def test_f_on_instance(self) -> None:
        """F works from an instance as well as the class."""
        vol = FakeVolume(uuid="abc")
        result = vol.F.name == "test"
        assert isinstance(result, Eq)


# ---------------------------------------------------------------------------
# QueryBuilder.filter() with FilterExpressions
# ---------------------------------------------------------------------------


class TestQueryBuilderFilterExpressions:
    def test_filter_expression_eq(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        fake_backend = MagicMock()
        fake_backend.query.return_value = []
        ds._backends["ontap"] = fake_backend

        list(ds.query(FakeVolume, cluster="prod1").filter(FakeVolume.F.svm.name == "vs1"))

        filters_arg = fake_backend.query.call_args_list[0].args[4]
        assert filters_arg == {"svm.name": "vs1"}

    def test_filter_expression_non_eq_adds_where(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        fake_backend = MagicMock()
        fake_backend.query.return_value = []
        ds._backends["ontap"] = fake_backend

        list(ds.query(FakeVolume, cluster="prod1", source="cache").filter(FakeVolume.F.size > 1000))

        kwargs = fake_backend.query.call_args.kwargs
        assert "size > 1000" in kwargs.get("where_expressions", ())

    def test_filter_mixed_expression_dict_kwargs(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        fake_backend = MagicMock()
        fake_backend.query.return_value = []
        ds._backends["ontap"] = fake_backend

        list(
            ds.query(FakeVolume, cluster="prod1", source="cache").filter(
                FakeVolume.F.svm.name == "vs1",
                {"state": "online"},
                name="vol1",
            )
        )

        call = fake_backend.query.call_args_list[0]
        filters_arg = call.args[4]
        assert filters_arg == {"svm.name": "vs1", "state": "online", "name": "vol1"}

    def test_filter_dict_form_still_works(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Existing dict-form filter calls are unchanged."""
        ds = DataSource(mock_config)
        fake_backend = MagicMock()
        fake_backend.query.return_value = []
        ds._backends["ontap"] = fake_backend

        list(ds.query(FakeVolume, cluster="prod1").filter({"svm.name": "vs1"}))

        filters_arg = fake_backend.query.call_args_list[0].args[4]
        assert filters_arg == {"svm.name": "vs1"}

    def test_filter_kwargs_only_still_works(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """filter(key=value) convenience still works."""
        ds = DataSource(mock_config)
        fake_backend = MagicMock()
        fake_backend.query.return_value = []
        ds._backends["ontap"] = fake_backend

        list(ds.query(FakeVolume, cluster="prod1").filter(state="online"))

        filters_arg = fake_backend.query.call_args_list[0].args[4]
        assert filters_arg == {"state": "online"}

    def test_filter_rejects_invalid_positional_arg(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        qb = ds.query(FakeVolume, cluster="prod1")
        with pytest.raises(TypeError, match="dict or FilterExpression"):
            qb.filter("not a valid arg")  # type: ignore[arg-type]
