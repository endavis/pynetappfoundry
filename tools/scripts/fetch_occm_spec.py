"""Fetch and assemble the OCCM API spec from a connector.

The OCCM API serves a Swagger 1.2 spec as a multi-file resource listing.
This script authenticates, fetches the index, then downloads each
resource declaration and combines them into a single JSON file.

During assembly, the script normalizes the spec:
- Strips HTML tags from operation summaries
- Removes Scala JVM serialization artifacts from models
- Normalizes basePath to a placeholder
- Namespaces divergent duplicate models per resource

Usage:
    uv run python tools/scripts/fetch_occm_spec.py \\
        --host 10.0.0.1 \\
        --email user@company.com \\
        --password 'secret' \\
        --output docs/example-config/apis/occm/all.json

    # With --no-verify to skip TLS certificate verification
    uv run python tools/scripts/fetch_occm_spec.py \\
        --host 10.0.0.1 \\
        --email user@company.com \\
        --password 'secret' \\
        --output docs/example-config/apis/occm/all.json \\
        --no-verify

    # Dry run: just fetch the index and show available paths
    uv run python tools/scripts/fetch_occm_spec.py \\
        --host 10.0.0.1 \\
        --email user@company.com \\
        --password 'secret' \\
        --dry-run
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# Scala JVM artifact models that leak through the Swagger 1.2 serialization.
# These are internal Scala types, not real API models.
_SCALA_ARTIFACT_MODELS = frozenset(
    {
        "Enumeration",
        "Value",
        "Regex",
        "Pattern",
        "PatternMessage",
    }
)

# Regex to match HTML tags for stripping from summaries.
_HTML_TAG_RE = re.compile(r"<[^>]+>")

# Placeholder basePath replacing the real connector IP.
_NORMALIZED_BASE_PATH = "http://{connector}/occm/api"


def build_opener(no_verify: bool) -> urllib.request.OpenerDirector:
    """Build a urllib opener with cookie support and optional TLS bypass."""
    cookie_jar = http.cookiejar.CookieJar()
    handlers: list[urllib.request.BaseHandler] = [
        urllib.request.HTTPCookieProcessor(cookie_jar),
    ]
    if no_verify:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        handlers.append(urllib.request.HTTPSHandler(context=ctx))
    return urllib.request.build_opener(*handlers)


def authenticate(
    opener: urllib.request.OpenerDirector,
    base_url: str,
    email: str,
    password: str,
) -> None:
    """Authenticate to the OCCM connector via POST /auth/login."""
    login_url = f"{base_url}/occm/api/auth/login"
    payload = json.dumps({"email": email, "password": password}).encode()
    req = urllib.request.Request(
        login_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        response = opener.open(req)
        status = response.getcode()
        if status not in (200, 204):
            print(f"ERROR: Auth returned status {status}", file=sys.stderr)
            sys.exit(1)
        print(f"Authenticated (HTTP {status})")
    except urllib.error.HTTPError as e:
        print(f"ERROR: Auth failed: HTTP {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)


def fetch_json(opener: urllib.request.OpenerDirector, url: str) -> dict[str, Any]:
    """Fetch a URL and parse the JSON response.

    All OCCM API spec endpoints return JSON objects, not arrays.
    """
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    response = opener.open(req)
    data: dict[str, Any] = json.loads(response.read().decode())
    return data


def fetch_index(opener: urllib.request.OpenerDirector, base_url: str) -> list[dict[str, Any]]:
    """Fetch the API index from /occm/api/api-docs/."""
    index_url = f"{base_url}/occm/api/api-docs/"
    print(f"Fetching index: {index_url}")
    data = fetch_json(opener, index_url)
    apis: list[dict[str, Any]] = data.get("apis", [])
    print(f"Found {len(apis)} API resources")
    return apis


def fetch_resource(
    opener: urllib.request.OpenerDirector,
    base_url: str,
    path: str,
) -> dict[str, Any] | None:
    """Fetch a single resource declaration.

    Path comes from the index (e.g., '/tenants').
    The spec URL is base_url + /occm/api/api-docs + path_as_resource_name.
    """
    # Convert path like '/azure-vsa:working-environments' to URL segment
    # Strip leading slash for the URL
    resource_name = path.lstrip("/")
    url = f"{base_url}/occm/api/api-docs/{resource_name}"
    try:
        data = fetch_json(opener, url)
        api_count = len(data.get("apis", []))
        model_count = len(data.get("models", {}))
        print(f"  {path}: {api_count} endpoints, {model_count} models")
        return data
    except urllib.error.HTTPError as e:
        print(f"  {path}: FAILED (HTTP {e.code})", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  {path}: FAILED ({e})", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------


def _strip_html(text: str) -> str:
    """Remove HTML tags from a string and clean up whitespace."""
    cleaned = _HTML_TAG_RE.sub("", text)
    # Collapse multiple spaces and strip leading/trailing dots added by OCCM
    cleaned = re.sub(r"\s+", " ", cleaned).strip().rstrip(".")
    return cleaned


def _is_scala_artifact_property(prop_name: str) -> bool:
    """Check if a property name is a Scala JVM serialization artifact."""
    return "scala$" in prop_name


def _resource_prefix(resource_path: str) -> str:
    """Derive a CamelCase prefix from a resource path for namespacing.

    Examples:
        '/aws-ha:volumes' -> 'AwsHa'
        '/onprem:working-environments' -> 'Onprem'
        '/occm:key-store' -> 'OccmKeyStore'
        '/fsx:volumes' -> 'Fsx'
        '/working-environments' -> ''  (common resource, no prefix)
    """
    path = resource_path.lstrip("/")

    # Split on colon: left side is the provider/category prefix
    if ":" in path:
        prefix_part = path.split(":")[0]
    else:
        # Common resources like /tenants, /working-environments get no prefix
        return ""

    # Convert 'aws-ha' -> 'AwsHa', 'occm' -> 'Occm'
    parts = prefix_part.split("-")
    return "".join(part.capitalize() for part in parts)


def _strip_scala_from_model(model_def: dict[str, Any]) -> dict[str, Any]:
    """Remove Scala artifact properties from a model definition."""
    props = model_def.get("properties", {})
    clean_props = {
        name: defn for name, defn in props.items() if not _is_scala_artifact_property(name)
    }

    # Also clean $ref values that point to Scala types
    for defn in clean_props.values():
        ref = defn.get("$ref", "")
        if "scala." in ref or "scala$" in ref:
            # Replace Scala collection refs with generic types
            defn.pop("$ref", None)
            defn["type"] = "object"

    if clean_props != props:
        cleaned = dict(model_def)
        cleaned["properties"] = clean_props
        # Update required list too
        if "required" in cleaned:
            cleaned["required"] = [
                r for r in cleaned["required"] if not _is_scala_artifact_property(r)
            ]
        return cleaned
    return model_def


def _normalize_base_path(resource: dict[str, Any]) -> None:
    """Replace the real connector IP in basePath with a placeholder (in-place)."""
    base_path = resource.get("basePath", "")
    if base_path and "/occm/api" in base_path:
        resource["basePath"] = _NORMALIZED_BASE_PATH


def _find_divergent_models(
    resources: dict[str, dict[str, Any]],
) -> dict[str, dict[str, list[str]]]:
    """Find models that share a name but have different definitions.

    Returns a dict mapping model_name -> {serialized_def: [source_paths]}.
    Only includes models with more than one distinct definition.
    """
    # model_name -> {serialized_def -> [source_paths]}
    model_variants: dict[str, dict[str, list[str]]] = {}

    for path, resource in resources.items():
        for model_name, model_def in resource.get("models", {}).items():
            key = json.dumps(model_def, sort_keys=True)
            if model_name not in model_variants:
                model_variants[model_name] = {}
            variants = model_variants[model_name]
            if key not in variants:
                variants[key] = []
            variants[key].append(path)

    # Keep only models with multiple distinct definitions
    return {name: variants for name, variants in model_variants.items() if len(variants) > 1}


def _namespace_divergent_model(
    model_name: str,
    resource_path: str,
) -> str:
    """Generate a namespaced model name for a divergent duplicate.

    Only the minority variant(s) get namespaced. The majority variant
    keeps the original name.
    """
    prefix = _resource_prefix(resource_path)
    if prefix:
        return f"{prefix}{model_name}"
    return model_name


def assemble_spec(
    resources: dict[str, dict[str, Any]],
    api_version: str,
) -> dict[str, Any]:
    """Assemble all resources into a single combined spec.

    Swagger 1.2 is inherently multi-file. We combine into a single
    JSON structure that preserves the original format with normalizations:

    1. HTML tags stripped from operation summaries
    2. Scala JVM artifact models removed
    3. basePath normalized to placeholder
    4. Divergent duplicate models namespaced by resource prefix
    """
    # Pre-compute which models diverge across resources
    divergent = _find_divergent_models(resources)

    # For divergent models, find the majority variant (keeps original name)
    # Minority variants get namespaced
    majority_variant: dict[str, str] = {}  # model_name -> serialized majority def
    for model_name, variants in divergent.items():
        # Sort by source count descending — largest group is the majority
        sorted_variants = sorted(variants.items(), key=lambda x: len(x[1]), reverse=True)
        majority_variant[model_name] = sorted_variants[0][0]

    combined_apis: dict[str, Any] = {}
    all_models: dict[str, dict[str, Any]] = {}
    model_sources: dict[str, list[str]] = {}
    renamed_models: dict[str, str] = {}  # "OldName@/resource" -> "NewName"
    removed_scala: list[str] = []
    html_cleaned = 0

    for path, resource in sorted(resources.items()):
        # Normalize basePath
        _normalize_base_path(resource)

        # Strip HTML from summaries
        for api in resource.get("apis", []):
            for operation in api.get("operations", []):
                summary = operation.get("summary", "")
                if "<" in summary:
                    operation["summary"] = _strip_html(summary)
                    html_cleaned += 1

        # Process models for this resource
        clean_models: dict[str, Any] = {}
        for model_name, model_def in resource.get("models", {}).items():
            # Skip Scala artifact models
            if model_name in _SCALA_ARTIFACT_MODELS:
                removed_scala.append(f"{model_name} (from {path})")
                continue

            # Clean Scala properties from remaining models
            model_def = _strip_scala_from_model(model_def)

            # Handle divergent duplicates
            final_name = model_name
            if model_name in divergent:
                this_def = json.dumps(model_def, sort_keys=True)
                if this_def != majority_variant[model_name]:
                    # This is a minority variant — namespace it
                    final_name = _namespace_divergent_model(model_name, path)
                    renamed_models[f"{model_name}@{path}"] = final_name

                    # Update $ref references within this resource's models
                    # and operations to use the new name
                    _update_refs_in_resource(resource, model_name, final_name)

            # Update model id to match final name
            if final_name != model_name:
                model_def = dict(model_def)
                model_def["id"] = final_name

            clean_models[final_name] = model_def

            # Track in allModels (first occurrence wins for identical dupes)
            if final_name not in all_models:
                all_models[final_name] = model_def
                model_sources[final_name] = [path]
            else:
                model_sources[final_name].append(path)

        # Replace resource models with cleaned version
        resource["models"] = clean_models
        combined_apis[path] = resource

    # Report duplicate models (identical ones that were merged)
    dupes = {k: v for k, v in model_sources.items() if len(v) > 1}

    # Build metadata
    metadata: dict[str, Any] = {
        "resourceCount": len(combined_apis),
        "modelCount": len(all_models),
        "duplicateModels": dict(sorted(dupes.items())),
        "normalizations": {
            "htmlSummariesCleaned": html_cleaned,
            "scalaArtifactsRemoved": sorted(set(removed_scala)),
            "divergentModelsRenamed": renamed_models,
        },
    }

    _print_normalization_report(
        html_cleaned,
        removed_scala,
        renamed_models,
        dupes,
    )

    return {
        "swaggerVersion": "1.2",
        "apiVersion": api_version,
        "apis": combined_apis,
        "allModels": all_models,
        "_metadata": metadata,
    }


def _update_refs_in_resource(
    resource: dict[str, Any],
    old_name: str,
    new_name: str,
) -> None:
    """Update all $ref and type references in a resource from old_name to new_name."""
    # Update in models
    for model_def in resource.get("models", {}).values():
        for prop_def in model_def.get("properties", {}).values():
            if prop_def.get("$ref") == old_name:
                prop_def["$ref"] = new_name
            items = prop_def.get("items", {})
            if isinstance(items, dict) and items.get("$ref") == old_name:
                items["$ref"] = new_name

    # Update in operation parameters and return types
    for api in resource.get("apis", []):
        for operation in api.get("operations", []):
            if operation.get("type") == old_name:
                operation["type"] = new_name
            items = operation.get("items", {})
            if isinstance(items, dict) and items.get("$ref") == old_name:
                items["$ref"] = new_name
            for param in operation.get("parameters", []):
                if param.get("type") == old_name:
                    param["type"] = new_name


def _print_normalization_report(
    html_cleaned: int,
    removed_scala: list[str],
    renamed_models: dict[str, str],
    dupes: dict[str, list[str]],
) -> None:
    """Print a summary of normalizations applied."""
    print("\n--- Normalization Report ---")
    print(f"  HTML tags stripped from {html_cleaned} operation summaries")
    print(f"  Scala artifacts removed: {len(set(removed_scala))} model instances")
    for entry in sorted(set(removed_scala)):
        print(f"    {entry}")
    print(f"  Divergent models renamed: {len(renamed_models)}")
    for original, renamed in sorted(renamed_models.items()):
        print(f"    {original} -> {renamed}")
    print(f"  basePath normalized to: {_NORMALIZED_BASE_PATH}")

    if dupes:
        print(f"\n  {len(dupes)} models defined in multiple resources (identical):")
        for name, sources in sorted(dupes.items()):
            print(f"    {name}: {', '.join(sources[:3])}{'...' if len(sources) > 3 else ''}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch and assemble the OCCM API spec from a connector.",
    )
    parser.add_argument("--host", required=True, help="OCCM connector IP or hostname")
    parser.add_argument("--email", required=True, help="Auth email address")
    parser.add_argument("--password", required=True, help="Auth password")
    parser.add_argument(
        "--output",
        default="docs/example-config/apis/occm/all.json",
        help="Output file path (default: docs/example-config/apis/occm/all.json)",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip TLS certificate verification",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only fetch the index, don't download resources",
    )
    parser.add_argument(
        "--protocol",
        default="http",
        choices=["http", "https"],
        help="Protocol to use (default: http)",
    )
    args = parser.parse_args()

    base_url = f"{args.protocol}://{args.host}"
    opener = build_opener(args.no_verify)

    # Authenticate
    authenticate(opener, base_url, args.email, args.password)

    # Fetch index
    index_apis = fetch_index(opener, base_url)

    if args.dry_run:
        print("\nAvailable API resources:")
        for api in index_apis:
            path = api.get("path", "")
            desc = api.get("description", "")
            line = f"  {path}"
            if desc:
                line += f"  ({desc})"
            print(line)
        return

    # Fetch each resource
    print("\nFetching resource declarations:")
    resources: dict[str, dict[str, Any]] = {}
    api_version = "unknown"

    for api in index_apis:
        path = api.get("path", "")
        if not path:
            continue
        resource = fetch_resource(opener, base_url, path)
        if resource:
            resources[path] = resource
            if api_version == "unknown":
                api_version = resource.get("apiVersion", "unknown")

    print(f"\nFetched {len(resources)}/{len(index_apis)} resources")

    # Assemble and normalize
    combined = assemble_spec(resources, api_version)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(combined, indent=2) + "\n")
    print(f"\nSpec written to {output_path}")
    print(
        f"  {combined['_metadata']['resourceCount']} resources, "
        f"{combined['_metadata']['modelCount']} models"
    )


if __name__ == "__main__":
    main()
