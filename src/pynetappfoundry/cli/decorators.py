"""CLI decorators for common patterns."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

import click

from pynetappfoundry.core.config import Config
from pynetappfoundry.core.logging import setup_logger

F = TypeVar("F", bound=Callable[..., Any])


def with_config(action: str) -> Callable[[F], F]:
    """Inject Config and clusters into command, handle common errors.

    Like infrafoundry's @with_orchestrator but for NetApp tools.

    Args:
        action: Description of the action for error messages.

    Returns:
        Decorated function with config and clusters injected.
    """

    def decorator(func: F) -> F:
        @click.pass_context
        @wraps(func)
        def wrapper(ctx: click.Context, *args: Any, **kwargs: Any) -> Any:
            config_dir = ctx.obj.get("config_dir", "config")
            output_dir = ctx.obj.get("output_dir", "")
            debug = ctx.obj.get("debug", False)
            filter_str = kwargs.pop("filter", None)
            live = kwargs.pop("live", False)

            # Build script_name from full command path (e.g., "licenses_get")
            parts: list[str] = []
            c: click.Context | None = ctx
            while c:
                if c.info_name and c.info_name != "nf":
                    parts.append(c.info_name)
                c = c.parent
            script_name = "_".join(reversed(parts)) or "unknown"

            # Setup logging
            setup_logger(script_name)

            if debug:
                for handler in logging.getLogger().handlers:
                    handler.setLevel(logging.DEBUG)

            try:
                # Parse filter
                filter_dict: dict[str, str] = {}
                if filter_str:
                    filter_dict = json.loads(filter_str)

                # Create config
                config = Config(
                    config_dir,
                    output_dir,
                    script_name=script_name,
                    no_cache=live,
                )
                clusters = config.get_clusters(filter_dict)

                return func(*args, config=config, clusters=clusters, **kwargs)

            except json.JSONDecodeError as e:
                raise click.ClickException(f"Invalid filter JSON: {e}") from e
            except Exception as e:
                raise click.ClickException(f"{action}: {e}") from e

        return wrapper  # type: ignore[return-value]

    return decorator
