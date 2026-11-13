"""Hand-written support for the generated Console operation classes (#735, ADR-0019).

The classes under ``pynetappfoundry.clients.console.generated`` call these helpers and
take a ``Dispatch`` at construction. Keep this module free of any client import, so the
generated code and the clients can both import it.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal, Protocol

TokenType = Literal["user", "service"] | None


class Dispatch(Protocol):
    """Sends one call through a client's wrapper, token handling included.

    ``token_type`` is the operation's ``x-token-type``, fixed at codegen time: ``"user"``,
    ``"service"`` or ``None`` when the operation accepts either.  ``call_kwargs`` are the
    arguments of ``APIWrapper.call_endpoint``.
    """

    def __call__(self, token_type: TokenType, /, **call_kwargs: Any) -> Any:
        """Call the endpoint and return the decoded response."""
        ...


def csv_param(value: str | Sequence[str] | None) -> str | None:
    """Return ``value`` as the comma-joined string the agent expects."""
    if value is None or isinstance(value, str):
        return value
    return ",".join(value)


def drop_none(params: dict[str, Any]) -> dict[str, Any]:
    """Return ``params`` without the entries whose value is ``None``."""
    return {k: v for k, v in params.items() if v is not None}


def expect_object(response: Any, operation: str) -> dict[str, Any]:
    """Return ``response`` if it is a JSON object, else raise ``TypeError``.

    The message names the operation and the type, never the content.
    """
    if not isinstance(response, dict):
        raise TypeError(f"Expected a JSON object from {operation}, got {type(response).__name__}")
    return response


def expect_list(response: Any, operation: str) -> list[Any]:
    """Return ``response`` if it is a JSON array, else raise ``TypeError``.

    The message names the operation and the type, never the content.
    """
    if not isinstance(response, list):
        raise TypeError(f"Expected a JSON array from {operation}, got {type(response).__name__}")
    return response
