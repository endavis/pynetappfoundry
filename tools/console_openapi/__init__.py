"""Build-time tool that converts NetApp BlueXP/Console docs to OpenAPI 3.0.3.

Source: https://github.com/NetAppDocs/console-automation (AsciiDoc).

This package is **not** part of the shipped ``pynetappfoundry`` distribution.
It exists solely to generate ``tools/console_openapi/generated/console_openapi.yaml``
from the upstream documentation.
"""

from __future__ import annotations

__all__ = ["__version__"]

__version__ = "0.1.0"
