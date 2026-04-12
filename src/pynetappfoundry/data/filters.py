"""Typed filter DSL for DataSource queries.

Provides a ``FieldProxy`` attribute-traversal proxy and a
``FilterExpression`` dataclass hierarchy that compile to the same
dict-based filter shape ``DataSource.query().filter()`` already accepts.

This is an additive layer — the existing ``dict[str, Any]`` form
remains fully supported.

Example::

    from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume

    # Typed DSL (new):
    OntapVolume.F.svm.name == "vs1"        # → Eq("svm.name", "vs1")
    OntapVolume.F.size > 1_073_741_824     # → Gt("size", 1073741824)
    OntapVolume.F.state.in_(["online"])     # → In("state", ("online",))
    ~(OntapVolume.F.autosize.mode == "off") # → Not(Eq("autosize.mode", "off"))
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------------
# FilterExpression hierarchy
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FilterExpression:
    """Base class for all filter expression nodes."""

    def __invert__(self) -> Not:
        """Negate this expression: ``~expr`` → ``Not(expr)``."""
        return Not(self)

    def __and__(self, other: FilterExpression) -> And:
        """Combine expressions: ``a & b`` → ``And((a, b))``."""
        return And((self, other))


@dataclass(frozen=True)
class Eq(FilterExpression):
    """Equality: ``field == value``."""

    field: str
    value: Any


@dataclass(frozen=True)
class Ne(FilterExpression):
    """Not-equal: ``field != value``."""

    field: str
    value: Any


@dataclass(frozen=True)
class Lt(FilterExpression):
    """Less-than: ``field < value``."""

    field: str
    value: Any


@dataclass(frozen=True)
class Gt(FilterExpression):
    """Greater-than: ``field > value``."""

    field: str
    value: Any


@dataclass(frozen=True)
class Le(FilterExpression):
    """Less-or-equal: ``field <= value``."""

    field: str
    value: Any


@dataclass(frozen=True)
class Ge(FilterExpression):
    """Greater-or-equal: ``field >= value``."""

    field: str
    value: Any


@dataclass(frozen=True)
class In(FilterExpression):
    """Membership: ``field in (v1, v2, ...)``."""

    field: str
    values: tuple[Any, ...]


@dataclass(frozen=True)
class NotIn(FilterExpression):
    """Non-membership: ``field not in (v1, v2, ...)``."""

    field: str
    values: tuple[Any, ...]


@dataclass(frozen=True)
class IsNull(FilterExpression):
    """Null check: ``field is null``."""

    field: str


@dataclass(frozen=True)
class Not(FilterExpression):
    """Logical negation: ``not expr``."""

    expr: FilterExpression


@dataclass(frozen=True)
class And(FilterExpression):
    """Logical conjunction: ``expr1 and expr2 and ...``."""

    exprs: tuple[FilterExpression, ...]


# ---------------------------------------------------------------------------
# FieldProxy — attribute traversal that builds dotted paths
# ---------------------------------------------------------------------------


class FieldProxy:
    """Attribute-traversal proxy that builds dotted field paths.

    Comparison operators return :class:`FilterExpression` subclasses
    rather than ``bool``, so ``__hash__`` is overridden to use
    ``id(self)`` (required when ``__eq__`` doesn't return ``bool``).
    """

    __slots__ = ("_path",)

    _path: str

    def __init__(self, path: str = "") -> None:
        object.__setattr__(self, "_path", path)

    def __getattr__(self, name: str) -> FieldProxy:
        new_path = f"{self._path}.{name}" if self._path else name
        return FieldProxy(new_path)

    # -- comparison operators → FilterExpression --------------------------

    def __eq__(self, other: object) -> Eq:  # type: ignore[override]
        return Eq(self._path, other)

    def __ne__(self, other: object) -> Ne:  # type: ignore[override]
        return Ne(self._path, other)

    def __lt__(self, other: object) -> Lt:
        return Lt(self._path, other)

    def __gt__(self, other: object) -> Gt:
        return Gt(self._path, other)

    def __le__(self, other: object) -> Le:
        return Le(self._path, other)

    def __ge__(self, other: object) -> Ge:
        return Ge(self._path, other)

    def __hash__(self) -> int:
        return id(self)

    # -- collection operators ---------------------------------------------

    def in_(self, values: Any) -> In:
        """Membership test: ``field in (v1, v2, ...)``."""
        return In(self._path, tuple(values))

    def not_in(self, values: Any) -> NotIn:
        """Non-membership test: ``field not in (v1, v2, ...)``."""
        return NotIn(self._path, tuple(values))

    def is_null(self) -> IsNull:
        """Null check: ``field is null``."""
        return IsNull(self._path)


# ---------------------------------------------------------------------------
# Descriptor — the ``.F`` attribute on OntapModel
# ---------------------------------------------------------------------------


class FieldProxyDescriptor:
    """Descriptor that returns a fresh :class:`FieldProxy` on every access.

    Installed as a ``ClassVar`` on :class:`OntapModel` so that
    ``Model.F.svm.name == "vs1"`` works from the class itself.
    """

    def __get__(self, obj: object, objtype: type | None = None) -> FieldProxy:
        return FieldProxy()


# ---------------------------------------------------------------------------
# Compiler — expression tree → (dict, tuple[str, ...])
# ---------------------------------------------------------------------------


def _quote(value: Any) -> str:
    """Quote *value* for a where-expression string.

    Strings are single-quoted; numeric types are left bare.
    """
    if isinstance(value, (int, float)):
        return str(value)
    return f"'{value}'"


def _quote_list(values: tuple[Any, ...]) -> str:
    """Comma-separated quoted values for ``IN`` / ``NOT IN``."""
    return ", ".join(_quote(v) for v in values)


def _compile_one(
    expr: FilterExpression,
    eq_dict: dict[str, Any],
    wheres: list[str],
) -> None:
    """Compile a single expression, mutating *eq_dict* and *wheres*."""
    if isinstance(expr, Eq):
        eq_dict[expr.field] = expr.value
    elif isinstance(expr, Ne):
        wheres.append(f"{expr.field} != {_quote(expr.value)}")
    elif isinstance(expr, Lt):
        wheres.append(f"{expr.field} < {_quote(expr.value)}")
    elif isinstance(expr, Gt):
        wheres.append(f"{expr.field} > {_quote(expr.value)}")
    elif isinstance(expr, Le):
        wheres.append(f"{expr.field} <= {_quote(expr.value)}")
    elif isinstance(expr, Ge):
        wheres.append(f"{expr.field} >= {_quote(expr.value)}")
    elif isinstance(expr, In):
        wheres.append(f"{expr.field} in ({_quote_list(expr.values)})")
    elif isinstance(expr, NotIn):
        wheres.append(f"{expr.field} not in ({_quote_list(expr.values)})")
    elif isinstance(expr, IsNull):
        wheres.append(f"{expr.field} is null")
    elif isinstance(expr, Not):
        _compile_not(expr, wheres)
    elif isinstance(expr, And):
        for child in expr.exprs:
            _compile_one(child, eq_dict, wheres)
    else:  # pragma: no cover
        msg = f"Unsupported expression type: {type(expr).__name__}"
        raise TypeError(msg)


def _compile_not(expr: Not, wheres: list[str]) -> None:
    """Compile a ``Not(...)`` expression into *wheres*.

    Special-cases ``Not(Eq(...))`` → ``field != value`` for readability;
    all other inner expressions get wrapped in ``not (...)``.
    """
    inner = expr.expr
    if isinstance(inner, Eq):
        wheres.append(f"{inner.field} != {_quote(inner.value)}")
    else:
        # Compile the inner expression, collect its where fragments,
        # and wrap them in a single ``not (...)`` group.
        inner_dict: dict[str, Any] = {}
        inner_wheres: list[str] = []
        _compile_one(inner, inner_dict, inner_wheres)
        # If the inner produced equality entries, convert them to
        # where-expressions for the negation wrapper.
        for field, value in inner_dict.items():
            inner_wheres.append(f"{field} = {_quote(value)}")
        combined = " and ".join(inner_wheres) if inner_wheres else ""
        if combined:
            wheres.append(f"not ({combined})")


def compile_filters(
    *expressions: FilterExpression,
) -> tuple[dict[str, Any], tuple[str, ...]]:
    """Compile filter expressions into the dict + where-tuple shape.

    Args:
        *expressions: One or more :class:`FilterExpression` objects.

    Returns:
        A ``(dict, tuple)`` pair where the dict contains equality
        filters (``{field: value}``) and the tuple contains
        where-expression strings for non-equality operators.
    """
    eq_dict: dict[str, Any] = {}
    wheres: list[str] = []
    for expr in expressions:
        _compile_one(expr, eq_dict, wheres)
    return eq_dict, tuple(wheres)
