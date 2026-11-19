"""Active IQ Digital Advisor backend for the unified DataSource accessor.

Implements :class:`DigitalAdvisorBackend`, a live-only backend over
:class:`pynetappfoundry.clients.digitaladvisor.api.DigitalAdvisorAPIClient` (ADR-0036,
ADR-0037). It has no cache database.

The backend builds each GraphQL document from the Pydantic models: a model field is a
selected field, a nested model a ``{ ... }`` sub-selection. The models hold only curated
fields; :data:`PERSONAL_DATA_FIELDS` is a second guard that refuses to select any
personal-data field, whatever a model holds. Documents go through
:meth:`DigitalAdvisorAPIClient.paginate`, so every one still passes ``ensure_read_only``.

Filters. A ``.filter()`` key that names a root-query argument of the mapping
(:data:`_SPECS`) is sent as a typed GraphQL variable, never interpolated into the
document. Every other key is an in-memory equality filter on a dotted path of the
record, as in the OCCM backend. An unknown top-level key raises ``ValueError`` before
any request, so a mistyped argument name cannot silently empty the result.
"""

from __future__ import annotations

import logging
import re
import types
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeVar, Union, get_args, get_origin

from pydantic import BaseModel

from pynetappfoundry.data.backends import Backend
from pynetappfoundry.utils.dict_path import PathNotFoundError, get_nested_value

if TYPE_CHECKING:
    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.clients.digitaladvisor.api import DigitalAdvisorAPIClient
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.data._routing import RoutingDecision

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

#: Field names that carry personal data. The backend never selects one of them.
PERSONAL_DATA_FIELDS: frozenset[str] = frozenset(
    {
        "contactPerson",
        "salesRepresentative",
        "csm",
        "retentionSpecialist",
        "solutionEngineerSpecialist",
        "sam",
        "streetAddress",
        "postalCode",
    }
)

_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_TOP_LEVEL_SPLIT = re.compile(r"[.\[]")


@dataclass(frozen=True)
class _QuerySpec:
    """How to query one root connection.

    Attributes:
        operation: Name of the GraphQL operation.
        connection: Root query field, also the key in ``data``.
        records_key: Name of the record list inside the connection.
        total_count: Whether the connection has a ``totalCount`` field.
        required: Required arguments: name to (GraphQL type, default value).
        optional: Optional arguments: filter key to GraphQL type.
        argument_names: Filter key to GraphQL argument name, for a key that differs
            from the argument. The argument name is also the variable name.
    """

    operation: str
    connection: str
    records_key: str
    total_count: bool
    required: dict[str, tuple[str, Any]] = field(default_factory=dict)
    optional: dict[str, str] = field(default_factory=dict)
    argument_names: dict[str, str] = field(default_factory=dict)


_SCOPE_ARGUMENTS: dict[str, str] = {
    "customerId": "String",
    "siteId": "String",
    "clusterId": "String",
    "watchlistId": "String",
    "clusterIds": "[String!]",
}

# The argument types come from the service's schema. The defaults of the required
# ``systems`` arguments are chosen, not measured: ``includeAllStates`` against
# ``systemStates`` has unknown semantics. ``platformType`` is a field of a System
# record, so the filter key is ``platformTypes``: ``systems`` takes it as the argument
# ``platformType``, ``clusters`` as ``platformTypes`` (#1124).
_SPECS: dict[str, _QuerySpec] = {
    "clusters": _QuerySpec(
        operation="ListClusters",
        connection="clusters",
        records_key="clusters",
        total_count=False,
        optional={**_SCOPE_ARGUMENTS, "platformTypes": "[SystemPlatformType!]"},
    ),
    "systems": _QuerySpec(
        operation="ListSystems",
        connection="systems",
        records_key="systems",
        total_count=True,
        required={
            "productTypes": ("[ProductType!]!", ["FILER"]),
            "systemStates": ("[SystemState!]!", ["ACTIVE"]),
            "includeAllStates": ("Boolean!", False),
            "includeStorageGridNodes": ("Boolean!", False),
        },
        optional={
            **_SCOPE_ARGUMENTS,
            "platformTypes": "[SystemPlatformType!]",
            "operatingMode": "[SystemOperatingMode!]",
        },
        argument_names={"platformTypes": "platformType"},
    ),
    "volumes": _QuerySpec(
        operation="ListVolumes",
        connection="volumes",
        records_key="volumes",
        total_count=True,
        optional={"clusterId": "String", "vserverId": "String", "aggregateId": "String"},
    ),
}


def _top_level(key: str) -> str:
    """Return the first path segment of a dotted filter *key*."""
    return _TOP_LEVEL_SPLIT.split(key, maxsplit=1)[0]


def _model_of(annotation: Any) -> type[BaseModel] | None:
    """Return the model class inside ``X | None`` or ``list[X]``, else ``None``."""
    origin = get_origin(annotation)
    if origin is Union or origin is types.UnionType or origin is list:
        for arg in get_args(annotation):
            found = _model_of(arg)
            if found is not None:
                return found
        return None
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return annotation
    return None


def selection_set(model_class: type[BaseModel], fields: frozenset[str] | None = None) -> str:
    """Return the GraphQL selection for *model_class*, generated from its fields.

    Args:
        model_class: The model whose fields are selected.
        fields: Top-level field names to keep (default: all). A nested model always
            brings its whole curated sub-selection.

    Raises:
        ValueError: If a name is not a valid GraphQL name, or is in
            :data:`PERSONAL_DATA_FIELDS`.
    """
    parts: list[str] = []
    for name, info in model_class.model_fields.items():
        if fields is not None and name not in fields:
            continue
        if name in PERSONAL_DATA_FIELDS:
            raise ValueError(
                f"{model_class.__name__}.{name} is personal data and is never selected"
            )
        if not _NAME_RE.match(name):
            raise ValueError(f"invalid GraphQL field name {name!r} in {model_class.__name__}")
        nested = _model_of(info.annotation)
        if nested is None:
            parts.append(name)
        else:
            parts.append(f"{name} {{ {selection_set(nested)} }}")
    return " ".join(parts)


def build_document(spec: _QuerySpec, selection: str, optional_used: list[str]) -> str:
    """Return the query document for *spec* with *selection*.

    Args:
        spec: The connection to query.
        selection: The record selection from :func:`selection_set`.
        optional_used: Names of the optional arguments to declare and pass.
    """
    declared = ["$pageSize: Int", "$after: String"]
    passed = ["pageSize: $pageSize", "after: $after"]
    for name, (gql_type, _default) in spec.required.items():
        declared.append(f"${name}: {gql_type}")
        passed.append(f"{name}: ${name}")
    for name in optional_used:
        argument = spec.argument_names.get(name, name)
        declared.append(f"${argument}: {spec.optional[name]}")
        passed.append(f"{argument}: ${argument}")
    total = "    totalCount\n" if spec.total_count else ""
    return (
        f"query {spec.operation}({', '.join(declared)}) {{\n"
        f"  {spec.connection}({', '.join(passed)}) {{\n"
        f"{total}    cursor\n    {spec.records_key} {{ {selection} }}\n"
        "  }\n}\n"
    )


def _matches(item: BaseModel, filters: dict[str, Any]) -> bool:
    """Return whether every equality filter matches *item* (missing path: no match)."""
    dumped = item.model_dump()
    for key, expected in filters.items():
        try:
            actual = get_nested_value(dumped, key)
        except PathNotFoundError:
            return False
        if actual != expected:
            return False
    return True


class DigitalAdvisorBackend(Backend):
    """Live-only backend that reads Active IQ Digital Advisor through its GraphQL client.

    There is one account (``digitaladvisorapi.toml``), so ``cluster`` is only a label
    and is otherwise ignored. ``where_expressions``, ``path_params`` and
    ``parent_filters`` are not supported.

    Args:
        config: The :class:`pynetappfoundry.core.config.Config` instance.
    """

    supports_where_expressions: bool = False
    supports_path_params: bool = False
    supports_parent_filters: bool = False
    # No cache: auto routing goes live, source="cache" is rejected.
    live_only: bool = True

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._api_client: DigitalAdvisorAPIClient | None = None

    def _get_api_client(self) -> DigitalAdvisorAPIClient:
        """Lazily create the Digital Advisor client, cached for the backend's lifetime."""
        if self._api_client is None:
            from pynetappfoundry.clients.digitaladvisor.api import DigitalAdvisorAPIClient

            self._api_client = DigitalAdvisorAPIClient(config=self._config)
        return self._api_client

    @staticmethod
    def _split_filters(
        model_class: type[BaseModel], spec: _QuerySpec, filters: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Split *filters* into query arguments and in-memory filters.

        Raises:
            ValueError: For a key that is neither an argument nor a model field.
        """
        arguments: dict[str, Any] = {}
        in_memory: dict[str, Any] = {}
        known = set(spec.required) | set(spec.optional)
        for key, value in filters.items():
            top = _top_level(key)
            if key in known:
                arguments[key] = value
            elif top in model_class.model_fields:
                in_memory[key] = value
            else:
                msg = (
                    f"{model_class.__name__}: unknown filter {key!r}; "
                    f"query arguments: {', '.join(sorted(known)) or 'none'}; "
                    f"fields: {', '.join(model_class.model_fields)}"
                )
                raise ValueError(msg)
        return arguments, in_memory

    def query(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        filters: dict[str, Any],
        *,
        where_expressions: tuple[str, ...] = (),
        path_params: dict[str, Any] | None = None,
    ) -> list[T]:
        """List the records of *mapping* and apply the in-memory filters.

        Raises:
            NotImplementedError: For ``where_expressions`` or a cache-only decision.
            ValueError: For ``path_params``, an unknown filter key, or a personal-data
                field in a model.
        """
        if where_expressions:
            msg = "Digital Advisor backend does not support where_expressions"
            raise NotImplementedError(msg)
        if path_params:
            msg = f"{mapping.name}: Digital Advisor backend does not support path_params"
            raise ValueError(msg)
        if decision.cache_fields and not decision.live_fields:
            msg = f"Digital Advisor backend has no cache; cannot serve {mapping.name} from it"
            raise NotImplementedError(msg)
        if not decision.live_fields:
            return []

        spec = _SPECS[mapping.api_endpoint]
        arguments, in_memory = self._split_filters(model_class, spec, filters)
        wanted = {_top_level(f) for f in decision.live_fields} | {_top_level(k) for k in in_memory}
        if isinstance(mapping.identifier_field, str):
            wanted.add(mapping.identifier_field)
        selection = selection_set(model_class, frozenset(wanted))

        optional_used = [name for name in spec.optional if name in arguments]
        variables: dict[str, Any] = {name: default for name, (_t, default) in spec.required.items()}
        variables.update({spec.argument_names.get(k, k): v for k, v in arguments.items()})
        document = build_document(spec, selection, optional_used)

        client = self._get_api_client()
        records = client.paginate(document, variables, spec.connection, spec.records_key)

        results: list[T] = []
        for record in records:
            item = model_class.model_validate(record)
            if not _matches(item, in_memory):
                continue
            fetched = getattr(item, "_fetched_fields", None)
            if fetched is not None:
                fetched.update(decision.live_fields)
            results.append(item)
        return results
