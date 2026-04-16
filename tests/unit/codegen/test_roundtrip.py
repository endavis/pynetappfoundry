"""Round-trip regression test for the OpenAPI codegen pipeline.

The codegen pipeline must be a no-op against the current on-disk output.
For each representative endpoint the test:

1. Seeds a temp directory with a copy of the on-disk ``<name>.toml``
   overlay (so :func:`generate_mapping` can mirror any
   ``cache_strategy`` / ``requires_explicit_fetch`` values the TOML
   declares).
2. Runs :func:`write_endpoint_files` into the temp directory (threading
   the spec-wide ``shared_schemas`` set — see ADR-0008).
3. Runs ``ruff format`` (via ``subprocess.run``) over the generated
   ``mapping.py`` and ``model.py`` — the on-disk files are formatted
   the same way, so any ordering differences surface here.
4. Diffs the produced files against the on-disk files and asserts
   byte-identical equality.

If any diff is found, the generator has drifted from the on-disk
expectation — either the generator has a bug or the on-disk file has
an un-mirrored hand edit.  Both are fail cases the maintainer must fix
before the codegen is safe to run against the full tree.

ONTAP endpoints (issue #601):

* ``/storage/volumes`` — biggest on-disk mapping, exercises
  ``cache_strategy="realtime"`` + ``requires_explicit_fetch`` mirroring,
  array-of-objects transforms, and ``identifier_field`` inference.
* ``/storage/aggregates`` — array-of-objects transforms plus
  ``cache_strategy`` mirroring, ``identifier_field`` inference.
* ``/svm/peers`` — simple flat mapping with only
  ``identifier_field`` inference, no transforms or TOML overrides.
* ``/network/fc/fabrics/{fabric.name}/zones`` — child endpoint whose
  parent (``/network/fc/fabrics``) uses ``identifier_field="name"``
  instead of the ONTAP default ``"uuid"``.  Exercises
  ``parent_id_field`` derivation from the identifier map (issue #606).

DII endpoints (issue #603):

* ``/assets/storages`` — flat DII endpoint, exercises non-ONTAP
  ``api_endpoint`` (no ``?fields=*``), ``api_type="dii"``,
  ``identifier_field="id"``, and a non-shared response schema
  (``Storage``, but still shared across 12 endpoints so URL-path-derived
  naming kicks in → class name ``DiiAssetsStorage``).
* ``/assets/storages/count`` — the headline shared-schema case.
  Response schema is ``Count``, referenced by 7 DII endpoints.  The
  shared-schema naming rule (ADR-0008, #603) produces the URL-path
  class name ``DiiAssetsStoragesCount`` instead of the colliding
  schema-derived ``DiiCount``.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from tools.codegen.adapters import detect_shared_schemas, parse_openapi_spec
from tools.codegen.generators import write_endpoint_files
from tools.codegen.openapi_codegen import _deduplicate_endpoints

# Resolve the repo root so the test is robust to pytest being invoked
# from any working directory.
REPO_ROOT = Path(__file__).resolve().parents[3]
ONTAP_SPEC_PATH = REPO_ROOT / "docs" / "example-config" / "apis" / "ontap" / "openapi3.json"
DII_SPEC_PATH = REPO_ROOT / "docs" / "example-config" / "apis" / "dii" / "openapi3.json"
CACHE_ROOT = REPO_ROOT / "src" / "pynetappfoundry" / "cache"
MODELS_ROOT = REPO_ROOT / "src" / "pynetappfoundry" / "models"


# (api_type, api_path, module_parts, toml_stem) — module_parts mirrors
# the on-disk directory layout.
ROUNDTRIP_ENDPOINTS = [
    ("ontap", "/storage/volumes", ("storage", "volumes"), "volumes"),
    ("ontap", "/storage/aggregates", ("storage", "aggregates"), "aggregates"),
    ("ontap", "/svm/peers", ("svm", "peers"), "peers"),
    # Child endpoint whose parent uses ``identifier_field="name"`` (#606).
    (
        "ontap",
        "/network/fc/fabrics/{fabric.name}/zones",
        ("network", "fc", "fabrics", "zones"),
        "zones",
    ),
    ("dii", "/assets/storages", ("assets", "storages"), "storages"),
    ("dii", "/assets/storages/count", ("assets", "storages", "count"), "count"),
]


@pytest.fixture(scope="module")
def parsed_endpoints_by_api() -> dict[str, tuple[list, set[str], list]]:
    """Parse each spec once per module and return (endpoints, shared_schemas, full_endpoints).

    Mirrors the production pipeline in :mod:`tools.codegen.openapi_codegen`:
    deduplicates same-module-path endpoints BEFORE detecting shared
    schemas.  ONTAP's collection+item pairs reference the same schema
    but only one survives dedup, so the schema is not truly shared
    across distinct module paths.

    Also returns the full (pre-dedup) endpoint list so the test can
    build ``schema_lookup`` and ``identifier_map`` from all endpoints —
    mirroring the production code which builds these from the full list
    so child endpoints can always find their parent's schema and
    identifier field (issue #606).
    """
    result: dict[str, tuple[list, set[str], list]] = {}
    for api_type, spec_path in [("ontap", ONTAP_SPEC_PATH), ("dii", DII_SPEC_PATH)]:
        if not spec_path.exists():
            continue
        full_endpoints = parse_openapi_spec(spec_path, api_type)
        endpoints = _deduplicate_endpoints(full_endpoints)
        shared = detect_shared_schemas(endpoints)
        result[api_type] = (endpoints, shared, full_endpoints)
    return result


def _ruff_format(*paths: Path) -> None:
    """Run ``ruff format`` on the given paths.

    The round-trip test is validated against ruff-formatted files on
    disk, so the generated output has to go through the same formatter
    before comparison.
    """
    subprocess.run(
        ["uv", "run", "ruff", "format", *[str(p) for p in paths]],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )


@pytest.mark.parametrize(
    ("api_type", "api_path", "module_parts", "toml_stem"),
    ROUNDTRIP_ENDPOINTS,
    ids=[f"{ep[0]}:{ep[1]}" for ep in ROUNDTRIP_ENDPOINTS],
)
def test_codegen_round_trip(
    api_type: str,
    api_path: str,
    module_parts: tuple[str, ...],
    toml_stem: str,
    parsed_endpoints_by_api: dict[str, tuple[list, set[str], list]],
    tmp_path: Path,
) -> None:
    """Regenerating an on-disk endpoint must reproduce it byte-identically."""
    if api_type not in parsed_endpoints_by_api:
        pytest.skip(f"{api_type} spec not available")
    endpoints, shared_schemas, full_endpoints = parsed_endpoints_by_api[api_type]
    endpoint = next((e for e in endpoints if e.path == api_path), None)
    assert endpoint is not None, f"endpoint {api_path} not found in parsed {api_type} spec"

    # On-disk targets
    ondisk_cache_dir = CACHE_ROOT / api_type / Path(*module_parts)
    ondisk_models_dir = MODELS_ROOT / api_type / Path(*module_parts)
    ondisk_mapping = ondisk_cache_dir / "mapping.py"
    ondisk_model = ondisk_models_dir / "model.py"
    ondisk_toml = ondisk_cache_dir / f"{toml_stem}.toml"

    assert ondisk_mapping.exists(), f"missing on-disk mapping: {ondisk_mapping}"
    assert ondisk_model.exists(), f"missing on-disk model: {ondisk_model}"
    assert ondisk_toml.exists(), f"missing on-disk TOML: {ondisk_toml}"

    # Seed the temp tree with a copy of the on-disk TOML so
    # ``generate_mapping`` can read its ``cache_strategy`` /
    # ``requires_explicit_fetch`` overrides when emitting Python.
    temp_cache_dir = tmp_path / "cache"
    temp_models_dir = tmp_path / "models"
    seed_dir = temp_cache_dir / api_type / Path(*module_parts)
    seed_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ondisk_toml, seed_dir / f"{toml_stem}.toml")

    # Build schema_lookup and identifier_map from the full (pre-dedup)
    # endpoint list — mirrors production code in openapi_codegen.py so
    # child endpoints can always resolve their parent's schema and
    # identifier field even when the parent was collapsed by dedup (#606).
    schema_lookup = {e.path: e.schema_name for e in full_endpoints}
    identifier_map = {e.path: e.identifier_field for e in full_endpoints if e.identifier_field}
    write_endpoint_files(
        endpoint,
        temp_cache_dir,
        api_type,
        None,
        schema_lookup,
        models_dir=temp_models_dir,
        shared_schemas=shared_schemas,
        identifier_map=identifier_map,
    )

    generated_mapping = temp_cache_dir / api_type / Path(*module_parts) / "mapping.py"
    generated_model = temp_models_dir / api_type / Path(*module_parts) / "model.py"

    assert generated_mapping.exists(), "codegen did not produce mapping.py"
    assert generated_model.exists(), "codegen did not produce model.py"

    # Format the generated files the same way the on-disk ones are.
    _ruff_format(generated_mapping, generated_model)

    # Byte-identical assertion: any drift is a generator bug or an
    # un-mirrored on-disk hand edit.
    ondisk_mapping_bytes = ondisk_mapping.read_bytes()
    generated_mapping_bytes = generated_mapping.read_bytes()
    assert generated_mapping_bytes == ondisk_mapping_bytes, (
        f"mapping.py drift for {api_path}:\n"
        f"  on-disk:   {ondisk_mapping}\n"
        f"  generated: {generated_mapping}\n"
    )

    ondisk_model_bytes = ondisk_model.read_bytes()
    generated_model_bytes = generated_model.read_bytes()
    assert generated_model_bytes == ondisk_model_bytes, (
        f"model.py drift for {api_path}:\n"
        f"  on-disk:   {ondisk_model}\n"
        f"  generated: {generated_model}\n"
    )
