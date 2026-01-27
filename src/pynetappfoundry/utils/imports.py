"""Import utility functions."""

from __future__ import annotations

import importlib
import inspect
import sys
from pathlib import Path
from types import ModuleType


def import_all_files(package_name: str, package_path: Path) -> None:
    """Import all Python files in a package and expose their members.

    Args:
        package_name: The name of the package.
        package_path: Path to the package directory.
    """
    for file in package_path.iterdir():
        if file.is_file() and file.suffix == ".py" and not file.name.startswith("__"):
            module_name = file.stem
            full_module_name = f"{package_name}.{module_name}"

            module: ModuleType = importlib.import_module(full_module_name)

            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) or inspect.isclass(obj):
                    setattr(sys.modules[package_name], name, obj)
