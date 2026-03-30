#!/usr/bin/env python3
"""One-time migration script: move model.py files from cache/ontap/ to models/ontap/.

This script:
1. Copies model.py files to models/ontap/{path}/model.py
2. Updates imports: CacheModel -> OntapModel
3. Creates __init__.py files for the models tree
4. Deletes old cache/ontap/{path}/model.py files
5. Updates cache/ontap/{path}/__init__.py to import from models.ontap
6. Updates cache/ontap/{path}/mapping.py to import from models.ontap
"""

from __future__ import annotations

import re
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src" / "pynetappfoundry"
CACHE_ONTAP = SRC / "cache" / "ontap"
MODELS_ONTAP = SRC / "models" / "ontap"

# Container model files that aggregate other models (not API endpoint models).
# These import from other model.py files and are NOT direct API endpoint models.
# They don't have mapping.py siblings. Identified by checking for
# models that import from OTHER model.py files within the same tree.
CONTAINER_MODEL_DIRS = {"storage", "network", "protocols"}


def relative_path(model_file: Path) -> Path:
    """Get path relative to cache/ontap/."""
    return model_file.relative_to(CACHE_ONTAP)


def find_all_model_files() -> list[Path]:
    """Find all model.py files under cache/ontap/."""
    return sorted(CACHE_ONTAP.rglob("model.py"))


def copy_model_to_models_pkg(model_file: Path) -> Path:
    """Copy a model.py to models/ontap/ and update imports."""
    rel = relative_path(model_file)
    dest = MODELS_ONTAP / rel
    dest.parent.mkdir(parents=True, exist_ok=True)

    content = model_file.read_text()

    # Replace CacheModel imports with OntapModel
    content = re.sub(
        r"from pynetappfoundry\.cache\._base import (.*)CacheModel(.*)",
        lambda m: _replace_cache_model_import(m.group(1), m.group(2)),
        content,
    )

    # Replace (CacheModel) in class definitions with (OntapModel)
    content = content.replace("(CacheModel)", "(OntapModel)")

    # Update cross-model imports: model.py files that import from other
    # cache.ontap.*.model -> models.ontap.*.model
    content = re.sub(
        r"from pynetappfoundry\.cache\.ontap\.([\w.]+)\.model import",
        r"from pynetappfoundry.models.ontap.\1.model import",
        content,
    )

    dest.write_text(content)
    return dest


def _replace_cache_model_import(before: str, after: str) -> str:
    """Build the replacement import line."""
    # Collect all names being imported
    names_str = before + "CacheModel" + after
    # Split by comma and clean up
    names = [n.strip().rstrip(",") for n in names_str.split(",") if n.strip()]
    # Replace CacheModel with OntapModel
    new_names = []
    for name in names:
        if name == "CacheModel":
            new_names.append("OntapModel")
        else:
            new_names.append(name)
    return f"from pynetappfoundry.models._base import {', '.join(sorted(new_names))}"


def create_init_file(pkg_dir: Path, class_name: str | None = None) -> None:
    """Create an __init__.py for a models/ontap/ sub-package."""
    init_file = pkg_dir / "__init__.py"
    if class_name:
        # Leaf package: re-export the primary model class
        rel_module = pkg_dir.relative_to(SRC).as_posix().replace("/", ".")
        content = (
            f'"""{class_name} model."""\n'
            f"\n"
            f"from {rel_module}.model import {class_name}\n"
            f"\n"
            f'__all__ = ["{class_name}"]\n'
        )
    else:
        # Intermediate package
        pkg_name = pkg_dir.name.replace("_", " ").title()
        content = f'"""{pkg_name} ONTAP models."""\n'

    init_file.write_text(content)


def get_primary_class_name(model_file: Path) -> str | None:
    """Extract the primary (last) class name from a model.py file."""
    content = model_file.read_text()
    classes = re.findall(r"^class (\w+)\(", content, re.MULTILINE)
    return classes[-1] if classes else None


def update_cache_init(init_file: Path) -> None:
    """Update a cache/ontap/__init__.py to import from models.ontap instead of local model."""
    if not init_file.exists():
        return

    content = init_file.read_text()

    # Determine the relative path from cache/ontap/
    rel_dir = init_file.parent.relative_to(CACHE_ONTAP)
    models_module = f"pynetappfoundry.models.ontap.{'.'.join(rel_dir.parts)}"

    # Replace import from .model or from pynetappfoundry.cache.ontap.{path}.model
    # to import from models.ontap.{path}.model
    cache_module = f"pynetappfoundry.cache.ontap.{'.'.join(rel_dir.parts)}.model"

    content = content.replace(
        f"from {cache_module}",
        f"from {models_module}.model",
    )

    init_file.write_text(content)


def update_cache_mapping(mapping_file: Path) -> None:
    """Update a cache/ontap/mapping.py to import models from models.ontap."""
    if not mapping_file.exists():
        return

    content = mapping_file.read_text()

    # Replace model imports from cache.ontap to models.ontap
    content = re.sub(
        r"from pynetappfoundry\.cache\.ontap\.([\w.]+)\.model import",
        r"from pynetappfoundry.models.ontap.\1.model import",
        content,
    )

    mapping_file.write_text(content)


def ensure_intermediate_inits(base_dir: Path, parts: list[str]) -> None:
    """Ensure __init__.py exists at every intermediate directory."""
    current = base_dir
    for part in parts:
        current = current / part
        current.mkdir(parents=True, exist_ok=True)
        init_file = current / "__init__.py"
        if not init_file.exists():
            pkg_name = part.replace("_", " ").title()
            init_file.write_text(f'"""{pkg_name} ONTAP models."""\n')


def main() -> None:
    """Run the migration."""
    model_files = find_all_model_files()
    print(f"Found {len(model_files)} model.py files to migrate")

    # Create models/ontap/ root
    MODELS_ONTAP.mkdir(parents=True, exist_ok=True)
    (MODELS_ONTAP / "__init__.py").write_text('"""ONTAP API models."""\n')

    migrated = 0
    for model_file in model_files:
        rel = relative_path(model_file)
        rel_parts = list(rel.parent.parts)  # e.g. ['storage', 'aggregates']

        # Ensure intermediate __init__.py files exist in models/ontap/
        ensure_intermediate_inits(MODELS_ONTAP, rel_parts)

        # Copy and transform model.py
        dest = copy_model_to_models_pkg(model_file)

        # Create __init__.py for the leaf package in models/ontap/
        class_name = get_primary_class_name(dest)
        create_init_file(dest.parent, class_name)

        # Delete old model.py from cache/ontap/
        model_file.unlink()

        # Update cache/ontap/__init__.py
        cache_init = model_file.parent / "__init__.py"
        update_cache_init(cache_init)

        # Update cache/ontap/mapping.py
        cache_mapping = model_file.parent / "mapping.py"
        update_cache_mapping(cache_mapping)

        migrated += 1
        if migrated % 50 == 0:
            print(f"  Migrated {migrated}/{len(model_files)}")

    print(f"Migration complete: {migrated} model files migrated")


if __name__ == "__main__":
    main()
