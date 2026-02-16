"""Codegen doit tasks for converting API specs to OpenAPI 3.x."""

import json
import shutil
import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import Any

from doit.tools import title_with_actions

# Spec directory relative to project root
_SPEC_DIR = Path("example-config/apis")

# Specs and their formats
_SPECS: dict[str, dict[str, str]] = {
    "ontap": {"format": "swagger_2", "source": "all.json"},
    "aiqum": {"format": "swagger_2", "source": "all.json"},
    "dii": {"format": "openapi_3", "source": "all.json"},
    "occm": {"format": "swagger_1", "source": "all.json"},
}

# Output filename for converted specs
_OUTPUT_FILENAME = "openapi3.json"


def _check_npx() -> None:
    """Check that npx is available."""
    if not shutil.which("npx"):
        print(
            "ERROR: npx is not installed. Install Node.js to get it:\n"
            "  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/"
            "install.sh | bash && nvm install --lts",
            file=sys.stderr,
        )
        raise RuntimeError("npx not found")


def _convert_swagger2_to_openapi3(source: Path, output: Path) -> None:
    """Convert a Swagger 2.0 spec to OpenAPI 3.0."""
    print(f"Converting {source} (Swagger 2.0 -> OpenAPI 3.0)...")
    result = subprocess.run(  # nosec B603 B607
        ["npx", "--yes", "swagger2openapi", "--patch", str(source), "-o", str(output)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"FAILED: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"swagger2openapi failed for {source}")
    print(f"  -> {output}")


def _convert_swagger1_to_openapi3(source: Path, output: Path) -> None:
    """Convert a Swagger 1.2 spec to OpenAPI 3.0 (two-step via Swagger 2.0).

    Step 1 uses a Python converter (tools/scripts/swagger12_to_20.py)
    since the assembled OCCM spec is a custom single-file format that
    api-spec-converter cannot parse. Step 2 uses swagger2openapi.
    """
    from tools.scripts.swagger12_to_20 import convert

    print(f"Converting {source} (Swagger 1.2 -> 2.0 -> OpenAPI 3.0)...")

    # Step 1: Swagger 1.2 -> Swagger 2.0 (Python)
    with open(source) as f:
        spec_12 = json.load(f)
    spec_20 = convert(spec_12)

    intermediate = output.parent / "swagger2_intermediate.json"
    intermediate.write_text(json.dumps(spec_20, indent=2) + "\n")
    paths = len(spec_20.get("paths", {}))
    definitions = len(spec_20.get("definitions", {}))
    print(f"  -> Swagger 2.0: {paths} paths, {definitions} definitions")

    # Step 2: Swagger 2.0 -> OpenAPI 3.0 (swagger2openapi)
    try:
        _convert_swagger2_to_openapi3(intermediate, output)
    finally:
        if intermediate.exists():
            intermediate.unlink()


def _convert_spec(api_name: str) -> None:
    """Convert a single API spec to OpenAPI 3.x."""
    spec_info = _SPECS[api_name]
    spec_dir = _SPEC_DIR / api_name
    source = spec_dir / spec_info["source"]
    output = spec_dir / _OUTPUT_FILENAME

    if not source.exists():
        print(f"SKIP: {source} does not exist")
        return

    fmt = spec_info["format"]
    if fmt == "openapi_3":
        # Already OpenAPI 3.x, just copy
        print(f"Copying {source} (already OpenAPI 3.x)...")
        shutil.copy2(source, output)
        print(f"  -> {output}")
    elif fmt == "swagger_2":
        _convert_swagger2_to_openapi3(source, output)
    elif fmt == "swagger_1":
        _convert_swagger1_to_openapi3(source, output)
    else:
        raise ValueError(f"Unknown format: {fmt}")


def _convert_all() -> None:
    """Convert all API specs to OpenAPI 3.x."""
    _check_npx()

    converted = 0
    skipped = 0
    failed = 0

    for api_name in sorted(_SPECS):
        try:
            _convert_spec(api_name)
            converted += 1
        except FileNotFoundError:
            print(f"SKIP: {api_name} - source spec not found")
            skipped += 1
        except RuntimeError as e:
            print(f"FAIL: {api_name} - {e}", file=sys.stderr)
            failed += 1

    print(f"\nDone: {converted} converted, {skipped} skipped, {failed} failed")
    if failed:
        raise RuntimeError(f"{failed} spec(s) failed to convert")


def task_convert_specs() -> dict[str, Any]:
    """Convert API specs to OpenAPI 3.x format.

    Usage:
        doit convert_specs              # Convert all specs
        doit convert_specs --api=ontap  # Convert a single spec
    """

    def run_convert(api: str) -> None:
        _check_npx()
        if api:
            if api not in _SPECS:
                available = ", ".join(sorted(_SPECS))
                raise ValueError(f"Unknown API: {api}. Available: {available}")
            _convert_spec(api)
        else:
            _convert_all()

    return {
        "actions": [run_convert],
        "title": title_with_actions,
        "verbosity": 2,
        "params": [
            {
                "name": "api",
                "short": "a",
                "long": "api",
                "type": str,
                "default": "",
                "help": "Convert a single API (ontap, aiqum, dii, occm). Omit to convert all.",
            },
        ],
    }
