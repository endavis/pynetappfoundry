#!/usr/bin/env python3
"""One-shot migration: strip parent prefixes from sub-model field names.

Sub-model fields were generated with the full api_path flattened, e.g.
``aggregates_name`` for api_path ``aggregates.name``.  They should use only the
leaf portion (``name``).  The sub-model class already provides namespacing.

This script:
1. Parses each model.py under models/ontap/
2. Identifies sub-model classes via their ``sub-model for {field_name}`` docstring
3. For each field in a sub-model class, strips the deepest matching prefix
4. Writes the updated file back
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MODELS_ROOT = (
    Path(__file__).resolve().parent.parent.parent / "src" / "pynetappfoundry" / "models" / "ontap"
)

# Regex to find sub-model docstrings like:  """ClassName sub-model for field_name."""
SUB_MODEL_DOC_RE = re.compile(r'""".*?sub-model for (\S+)\."""')

# Regex to match a field declaration line:  some_attr: type = default
FIELD_LINE_RE = re.compile(r"^(\s+)(\w+)(:\s+.+)$")


def _compute_prefix(field_name: str, api_paths_hint: list[str] | None = None) -> str:
    """Return the prefix to strip from sub-model field attrs.

    The codegen previously did: api_path.replace('.', '_').replace('-', '_')
    For a sub-model with docstring field_name='aggregates', a field with
    api_path 'aggregates.name' became 'aggregates_name'.

    For nested sub-models like field_name='suspect_files' under parent
    'anti_ransomware', the api_path might be 'anti_ransomware.suspect_files.count'
    which flattened to 'anti_ransomware_suspect_files_count'.

    We need to figure out what prefix to strip.  The prefix is everything up
    to and including the field_name segment in the flattened api_path.
    """
    return field_name.replace(".", "_").replace("-", "_") + "_"


def migrate_file(path: Path, *, dry_run: bool = False) -> bool:
    """Migrate a single model.py file. Returns True if changes were made."""
    text = path.read_text()
    lines = text.splitlines(keepends=True)

    # First pass: find all sub-model classes and their field_name prefixes
    # We track which line ranges belong to each sub-model class
    sub_model_ranges: list[tuple[int, str]] = []  # (start_line_idx, field_name)

    for i, line in enumerate(lines):
        m = SUB_MODEL_DOC_RE.search(line)
        if m:
            field_name = m.group(1)
            sub_model_ranges.append((i, field_name))

    if not sub_model_ranges:
        return False

    # For each sub-model, find the prefix from the docstring's field_name
    # We need to figure out the FULL prefix by looking at the actual field names
    # in the class body.
    #
    # Strategy: for each sub-model class, find all field lines and determine
    # the common prefix that matches the flattened api_path pattern.

    changed = False
    new_lines = list(lines)

    for _range_idx, (doc_line_idx, field_name) in enumerate(sub_model_ranges):
        # Find the end of this sub-model class (next class definition or end of file)
        next_class_idx = len(lines)
        for j in range(doc_line_idx + 1, len(lines)):
            if lines[j].startswith("class "):
                next_class_idx = j
                break

        # Collect all field lines in this sub-model class
        # We need to determine what prefix was used.
        # The field_name from docstring tells us the immediate parent.
        # But for deeply nested sub-models, the prefix includes ancestors too.
        #
        # Look at actual field names to find the prefix pattern.
        # All fields should share a common prefix that ends with field_name + "_"

        field_lines_in_class: list[tuple[int, re.Match[str]]] = []
        for j in range(doc_line_idx + 1, next_class_idx):
            m = FIELD_LINE_RE.match(lines[j])
            if m and m.group(2) != "pass":
                field_lines_in_class.append((j, m))

        if not field_lines_in_class:
            continue

        # Determine prefix: find the longest common prefix among all field names
        # that ends with field_name + "_"
        field_names_flat = field_name.replace(".", "_").replace("-", "_")

        # Find the actual prefix used. All field attrs should contain
        # the field_name portion followed by "_". Find where it appears.
        first_attr = field_lines_in_class[0][1].group(2)

        # The prefix is everything up to and including the last occurrence of
        # field_names_flat + "_" in the attr name.
        # E.g., for field_name="suspect_files" and attr="anti_ransomware_suspect_files_count"
        # the prefix is "anti_ransomware_suspect_files_"
        prefix_end = first_attr.find(field_names_flat + "_")
        if prefix_end == -1:
            # Field name IS the entire attr (no suffix) - can't strip
            # Or the pattern doesn't match - skip
            continue

        actual_prefix = first_attr[: prefix_end + len(field_names_flat) + 1]

        # Verify all fields in this class share this prefix
        all_match = True
        for _, fm in field_lines_in_class:
            attr = fm.group(2)
            if not attr.startswith(actual_prefix):
                all_match = False
                break

        if not all_match:
            # Try just field_names_flat + "_" as prefix (simpler case)
            actual_prefix = field_names_flat + "_"
            all_match = all(fm.group(2).startswith(actual_prefix) for _, fm in field_lines_in_class)
            if not all_match:
                # Some fields don't match - skip this class to be safe
                msg = f"  WARNING: Skipping {path}:{doc_line_idx + 1}"
                print(f"{msg} - inconsistent prefix for {field_name}")
                continue

        # Now strip the prefix from all field lines
        seen_new_attrs: set[str] = set()
        for j, fm in field_lines_in_class:
            old_attr = fm.group(2)
            new_attr = old_attr[len(actual_prefix) :]
            if not new_attr:
                # Stripping prefix would leave empty attr - skip
                continue

            # Handle potential duplicates after prefix removal
            if new_attr in seen_new_attrs:
                print(
                    f"  WARNING: Duplicate attr '{new_attr}' after prefix removal in {path}:{j + 1}"
                )
                continue
            seen_new_attrs.add(new_attr)

            if old_attr != new_attr:
                indent = fm.group(1)
                rest = fm.group(3)
                new_lines[j] = (
                    f"{indent}{new_attr}{rest}\n"
                    if lines[j].endswith("\n")
                    else f"{indent}{new_attr}{rest}"
                )
                changed = True

    if changed and not dry_run:
        path.write_text("".join(new_lines))

    return changed


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    count = 0

    for model_path in sorted(MODELS_ROOT.rglob("model.py")):
        if migrate_file(model_path, dry_run=dry_run):
            count += 1
            if dry_run:
                print(f"  WOULD change: {model_path}")

    action = "Would change" if dry_run else "Changed"
    print(f"\n{action} {count} model files.")


if __name__ == "__main__":
    main()
