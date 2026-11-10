"""Command error type with a single exit convention.

See ADR-0022 (``docs/decisions/0022-one-cli-error-exit-convention-raise-clierror.md``).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import IO, Any

import click

from pynetappfoundry.cli.utils import console, is_debug_mode, print_error, print_exception


class CliError(click.ClickException):
    """A command error that exits with ``exit_code`` and prints a red message.

    Unlike a plain ``ClickException`` the message goes to stdout through the
    shared console, in red, exactly like ``print_error``. Optional ``hints``
    are printed after the message as Rich markup lines. With ``exc`` the
    traceback is logged, and printed when ``--debug`` was active.

    Args:
        message: Error text (printed escaped).
        exit_code: Process exit code (1 by default, 2 for grep-style commands).
        hints: Extra Rich-markup lines printed after the message.
        exc: Underlying exception to log (and show in debug mode).
    """

    def __init__(
        self,
        message: str,
        exit_code: int = 1,
        *,
        hints: Sequence[str] = (),
        exc: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        # click types exit_code as ClassVar[int]; click itself reads it per instance.
        self.exit_code = exit_code  # type: ignore[misc]
        self.hints: tuple[str, ...] = tuple(hints)
        self.exc = exc
        # click calls show() after the context is popped, so capture debug now.
        self.debug = is_debug_mode()

    def show(self, file: IO[Any] | None = None) -> None:
        """Print the message and hints to the shared console (``file`` is ignored)."""
        if self.exc is not None:
            print_exception(self.message, self.exc, debug=self.debug)
        else:
            print_error(self.message)
        for hint in self.hints:
            console.print(hint)
