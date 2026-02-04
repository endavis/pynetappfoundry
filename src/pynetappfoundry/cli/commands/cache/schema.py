"""Cache schema command for displaying the cache metadata structure."""

from __future__ import annotations

import json
from typing import Any, TypeGuard, get_args, get_origin

import click
from pydantic import BaseModel
from rich.console import Console
from rich.tree import Tree

from pynetappfoundry.cache.models import CachedClusterMetadata

console = Console()


def _get_type_name(annotation: Any) -> str:
    """Get a human-readable type name from a type annotation.

    Args:
        annotation: Type annotation to convert.

    Returns:
        Human-readable type name.
    """
    origin = get_origin(annotation)
    if origin is list:
        args = get_args(annotation)
        if args:
            inner = _get_type_name(args[0])
            return f"list[{inner}]"
        return "list"
    if origin is dict:
        args = get_args(annotation)
        if len(args) == 2:
            return f"dict[{_get_type_name(args[0])}, {_get_type_name(args[1])}]"
        return "dict"

    # Handle Pydantic models
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return annotation.__name__

    # Handle basic types
    if hasattr(annotation, "__name__"):
        return str(annotation.__name__)

    return str(annotation)


def _is_pydantic_model(annotation: Any) -> TypeGuard[type[BaseModel]]:
    """Check if an annotation is a Pydantic model class.

    Args:
        annotation: Type annotation to check.

    Returns:
        True if it's a Pydantic model.
    """
    return isinstance(annotation, type) and issubclass(annotation, BaseModel)


def _get_list_item_type(annotation: Any) -> Any | None:
    """Get the item type from a list annotation.

    Args:
        annotation: List type annotation.

    Returns:
        The item type, or None if not a list.
    """
    origin = get_origin(annotation)
    if origin is list:
        args = get_args(annotation)
        if args:
            return args[0]
    return None


def _build_schema_tree(
    tree: Tree,
    model: type[BaseModel],
    prefix: str = "",
    visited: set[str] | None = None,
) -> None:
    """Build a Rich tree showing the schema structure.

    Args:
        tree: Rich Tree to populate.
        model: Pydantic model class to introspect.
        prefix: Dot-notation prefix for field paths.
        visited: Set of visited model names to prevent infinite recursion.
    """
    if visited is None:
        visited = set()

    model_name = model.__name__
    if model_name in visited:
        tree.add("[dim](recursive reference)[/dim]")
        return
    visited = visited | {model_name}

    for field_name, field_info in model.model_fields.items():
        annotation = field_info.annotation
        type_name = _get_type_name(annotation)
        full_path = f"{prefix}{field_name}" if prefix else field_name

        # Check if this is a nested Pydantic model
        if _is_pydantic_model(annotation):
            branch = tree.add(f"[cyan]{field_name}[/cyan]: [yellow]{type_name}[/yellow]")
            _build_schema_tree(branch, annotation, f"{full_path}.", visited)
        # Check if this is a list of Pydantic models
        elif get_origin(annotation) is list:
            item_type = _get_list_item_type(annotation)
            if item_type is not None and _is_pydantic_model(item_type):
                branch = tree.add(
                    f"[cyan]{field_name}[/cyan]: [yellow]{type_name}[/yellow] "
                    f"[dim](use {field_name}[N].field)[/dim]"
                )
                _build_schema_tree(branch, item_type, f"{full_path}[N].", visited)
            else:
                tree.add(f"[cyan]{field_name}[/cyan]: [green]{type_name}[/green]")
        else:
            tree.add(f"[cyan]{field_name}[/cyan]: [green]{type_name}[/green]")


def _build_flat_schema(
    model: type[BaseModel],
    prefix: str = "",
    visited: set[str] | None = None,
) -> list[tuple[str, str]]:
    """Build a flat list of field paths and types.

    Args:
        model: Pydantic model class to introspect.
        prefix: Dot-notation prefix for field paths.
        visited: Set of visited model names to prevent infinite recursion.

    Returns:
        List of (path, type_name) tuples.
    """
    if visited is None:
        visited = set()

    model_name = model.__name__
    if model_name in visited:
        return []
    visited = visited | {model_name}

    result: list[tuple[str, str]] = []

    for field_name, field_info in model.model_fields.items():
        annotation = field_info.annotation
        type_name = _get_type_name(annotation)
        full_path = f"{prefix}{field_name}" if prefix else field_name

        if _is_pydantic_model(annotation):
            result.extend(_build_flat_schema(annotation, f"{full_path}.", visited))
        elif get_origin(annotation) is list:
            item_type = _get_list_item_type(annotation)
            if item_type is not None and _is_pydantic_model(item_type):
                result.extend(_build_flat_schema(item_type, f"{full_path}[N].", visited))
            else:
                result.append((full_path, type_name))
        else:
            result.append((full_path, type_name))

    return result


@click.command()
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON schema.",
)
@click.option(
    "--flat",
    "output_flat",
    is_flag=True,
    help="Output as flat list of queryable paths.",
)
def schema(output_json: bool, output_flat: bool) -> None:
    """Display the cache metadata schema.

    Shows the structure of cached cluster metadata, including all fields
    and their types. Use this to discover available fields for querying
    with 'nf cache query'.

    \b
    Examples:
        nf cache schema              # Show schema as tree
        nf cache schema --flat       # Show flat list of paths
        nf cache schema --json       # Output JSON schema
    """
    if output_json:
        # Output the full JSON schema from Pydantic
        # Use click.echo instead of console.print to avoid Rich formatting
        json_schema = CachedClusterMetadata.model_json_schema()
        click.echo(json.dumps(json_schema, indent=2))
    elif output_flat:
        # Output flat list of queryable paths
        paths = _build_flat_schema(CachedClusterMetadata)
        console.print("\n[bold]Queryable Field Paths:[/bold]\n")
        for path, type_name in paths:
            console.print(f"  [cyan]{path}[/cyan]: [green]{type_name}[/green]")
        console.print()
        console.print("[dim]Use with: nf cache query <cluster> <path>[/dim]")
        console.print("[dim]For arrays, replace [N] with index (e.g., nodes[0].name)[/dim]")
    else:
        # Output as tree
        tree = Tree("[bold blue]CachedClusterMetadata[/bold blue]")
        _build_schema_tree(tree, CachedClusterMetadata)
        console.print()
        console.print(tree)
        console.print()
        console.print("[dim]Use 'nf cache schema --flat' to see queryable paths[/dim]")
