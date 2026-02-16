"""Codegen doit tasks for fetching, converting, and generating from API specs."""

import json
import shutil
import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import Any

from doit.tools import title_with_actions

# Spec directory relative to project root
_SPEC_DIR = Path("example-config/apis")

# APIs that support fetching, with their auth type
_FETCH_APIS = {
    "ontap": "basic",
    "aiqum": "basic",
    "dii": "apikey",
    "occm": "session",
}

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


def _fetch_spec(
    api: str,
    host: str,
    username: str,
    password: str,
    api_key: str,
    no_verify: bool,
) -> None:
    """Fetch a single API spec."""
    if api not in _FETCH_APIS:
        available = ", ".join(sorted(_FETCH_APIS))
        raise ValueError(f"Unknown API: {api}. Available: {available}")

    auth_type = _FETCH_APIS[api]

    if auth_type == "basic" and (not username or not password):
        raise ValueError(f"{api} requires --username and --password")
    if auth_type == "apikey" and not api_key:
        raise ValueError(f"{api} requires --api-key")
    if auth_type == "session" and (not username or not password):
        raise ValueError(f"{api} requires --username (email) and --password")
    if not host:
        raise ValueError("--host is required")

    if api == "ontap":
        from tools.scripts.fetch_ontap_spec import _sanitize_spec as sanitize_ontap
        from tools.scripts.fetch_ontap_spec import fetch_spec as fetch_ontap

        spec = fetch_ontap(host, username, password, no_verify)
        spec = sanitize_ontap(spec)
    elif api == "aiqum":
        from tools.scripts.fetch_aiqum_spec import _sanitize_spec as sanitize_aiqum
        from tools.scripts.fetch_aiqum_spec import fetch_spec as fetch_aiqum

        spec = fetch_aiqum(host, username, password, no_verify)
        spec = sanitize_aiqum(spec)
    elif api == "dii":
        from tools.scripts.fetch_dii_spec import _sanitize_spec as sanitize_dii
        from tools.scripts.fetch_dii_spec import fetch_spec as fetch_dii

        spec = fetch_dii(host, api_key, no_verify)
        spec = sanitize_dii(spec)
    elif api == "occm":
        from tools.scripts.fetch_occm_spec import (
            assemble_spec,
            authenticate,
            build_opener,
            fetch_index,
            fetch_resource,
        )

        protocol = "https" if no_verify else "http"
        base_url = f"{protocol}://{host}"
        opener = build_opener(no_verify)
        authenticate(opener, base_url, username, password)
        index_apis = fetch_index(opener, base_url)

        print("\nFetching resource declarations:")
        resources: dict[str, dict[str, Any]] = {}
        api_version = "unknown"
        for api_entry in index_apis:
            path = api_entry.get("path", "")
            if not path:
                continue
            resource = fetch_resource(opener, base_url, path)
            if resource:
                resources[path] = resource
                if api_version == "unknown":
                    api_version = resource.get("apiVersion", "unknown")

        print(f"\nFetched {len(resources)}/{len(index_apis)} resources")
        spec = assemble_spec(resources, api_version)

    output = _SPEC_DIR / api / "all.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(spec, indent=2) + "\n")
    print(f"\nSpec written to {output}")


def task_fetch_spec() -> dict[str, Any]:
    """Fetch an API spec from a live endpoint.

    Usage:
        doit fetch_spec --api=ontap --host=10.0.0.1 --username=admin --password=secret
        doit fetch_spec --api=aiqum --host=aiqum.local --username=admin --password=secret
        doit fetch_spec --api=dii --host=tenant.cloudinsights.netapp.com --api-key=TOKEN
        doit fetch_spec --api=occm --host=connector.local --username=user@co.com --password=secret
    """

    def run_fetch(
        api: str,
        host: str,
        username: str,
        password: str,
        api_key: str,
        no_verify: bool,
    ) -> None:
        if not api:
            available = ", ".join(sorted(_FETCH_APIS))
            raise ValueError(f"--api is required. Available: {available}")
        _fetch_spec(api, host, username, password, api_key, no_verify)

    return {
        "actions": [run_fetch],
        "title": title_with_actions,
        "verbosity": 2,
        "params": [
            {
                "name": "api",
                "short": "a",
                "long": "api",
                "type": str,
                "default": "",
                "help": "API to fetch (ontap, aiqum, dii, occm).",
            },
            {
                "name": "host",
                "short": "H",
                "long": "host",
                "type": str,
                "default": "",
                "help": "Hostname or IP of the API endpoint.",
            },
            {
                "name": "username",
                "short": "u",
                "long": "username",
                "type": str,
                "default": "",
                "help": "Username for basic/session auth (email for OCCM).",
            },
            {
                "name": "password",
                "short": "p",
                "long": "password",
                "type": str,
                "default": "",
                "help": "Password for basic/session auth.",
            },
            {
                "name": "api_key",
                "short": "k",
                "long": "api-key",
                "type": str,
                "default": "",
                "help": "API key for DII auth.",
            },
            {
                "name": "no_verify",
                "long": "no-verify",
                "type": bool,
                "default": False,
                "help": "Skip TLS certificate verification.",
            },
        ],
    }


# Default output directory for generated cache models
_CACHE_OUTPUT_DIR = Path("src/pynetappfoundry/cache")


def task_generate_models() -> dict[str, Any]:
    """Generate cache models and mappings from OpenAPI specs.

    Usage:
        doit generate_models --api=ontap   # Generate from ONTAP spec
        doit generate_models               # Generate from all specs
        doit generate_models --dry-run     # Preview without writing
    """

    def run_generate(api: str, dry_run: bool, endpoints: str) -> None:
        from tools.codegen.openapi_codegen import run

        api_list = [api] if api else sorted(_SPECS)

        for api_name in api_list:
            spec_path = _SPEC_DIR / api_name / _OUTPUT_FILENAME
            if not spec_path.exists():
                print(f"SKIP: {spec_path} does not exist (run 'doit convert_specs' first)")
                continue

            endpoint_filter = endpoints.split(",") if endpoints else None
            run(
                spec=spec_path,
                output=_CACHE_OUTPUT_DIR,
                api_type=api_name,
                endpoint_filter=endpoint_filter,
                dry_run=dry_run,
            )

    return {
        "actions": [run_generate],
        "title": title_with_actions,
        "verbosity": 2,
        "params": [
            {
                "name": "api",
                "short": "a",
                "long": "api",
                "type": str,
                "default": "",
                "help": "Generate for a single API (ontap, aiqum, dii, occm). Omit for all.",
            },
            {
                "name": "dry_run",
                "long": "dry-run",
                "type": bool,
                "default": False,
                "help": "Preview what would be generated without writing files.",
            },
            {
                "name": "endpoints",
                "long": "endpoints",
                "type": str,
                "default": "",
                "help": "Comma-separated endpoint paths to generate (e.g. /storage/volumes).",
            },
        ],
    }
