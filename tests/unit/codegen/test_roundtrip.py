"""Round-trip regression test for the OpenAPI codegen pipeline (issue #601).

The codegen pipeline must be a no-op against the current on-disk output.
For each of three representative ONTAP endpoints the test:

1. Seeds a temp directory with a copy of the on-disk ``<name>.toml``
   overlay (so :func:`generate_mapping` can mirror any
   ``cache_strategy`` / ``requires_explicit_fetch`` values the TOML
   declares).
2. Runs :func:`write_endpoint_files` into the temp directory.
3. Runs ``ruff format`` (via ``subprocess.run``) over the generated
   ``mapping.py`` and ``model.py`` — the on-disk files are formatted
   the same way, so any ordering differences surface here.
4. Diffs the produced files against the on-disk files and asserts
   byte-identical equality.

If any diff is found, the generator has drifted from the on-disk
expectation — either the generator has a bug or the on-disk file has
an un-mirrored hand edit.  Both are fail cases the maintainer must fix
before the codegen is safe to run across the full ONTAP tree.

Endpoints chosen:

* ``/storage/volumes`` — biggest on-disk mapping, exercises
  ``cache_strategy="realtime"`` + ``requires_explicit_fetch`` mirroring,
  array-of-objects transforms, and ``identifier_field`` inference.
* ``/storage/aggregates`` — array-of-objects transforms plus
  ``cache_strategy`` mirroring, ``identifier_field`` inference.
* ``/svm/peers`` — simple flat mapping with only
  ``identifier_field`` inference, no transforms or TOML overrides.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from tools.codegen.adapters import parse_openapi_spec
from tools.codegen.generators import write_endpoint_files

# Resolve the repo root so the test is robust to pytest being invoked
# from any working directory.
REPO_ROOT = Path(__file__).resolve().parents[3]
SPEC_PATH = REPO_ROOT / "docs" / "example-config" / "apis" / "ontap" / "openapi3.json"
CACHE_ROOT = REPO_ROOT / "src" / "pynetappfoundry" / "cache"
MODELS_ROOT = REPO_ROOT / "src" / "pynetappfoundry" / "models"


# (api_path, module_parts, toml_stem) — module_parts mirrors the
# on-disk directory layout.
ROUNDTRIP_ENDPOINTS = [
    ("/storage/volumes", ("storage", "volumes"), "volumes"),
    ("/storage/aggregates", ("storage", "aggregates"), "aggregates"),
    ("/svm/peers", ("svm", "peers"), "peers"),
]


@pytest.fixture(scope="module")
def parsed_endpoints():
    """Parse the ONTAP spec once per module."""
    if not SPEC_PATH.exists():
        pytest.skip(f"ONTAP spec not available at {SPEC_PATH}")
    endpoints = parse_openapi_spec(SPEC_PATH, "ontap")
    return endpoints


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
    ("api_path", "module_parts", "toml_stem"),
    ROUNDTRIP_ENDPOINTS,
    ids=[ep[0] for ep in ROUNDTRIP_ENDPOINTS],
)
def test_codegen_round_trip(
    api_path: str,
    module_parts: tuple[str, ...],
    toml_stem: str,
    parsed_endpoints,
    tmp_path: Path,
) -> None:
    """Regenerating an on-disk endpoint must reproduce it byte-identically."""
    endpoint = next((e for e in parsed_endpoints if e.path == api_path), None)
    assert endpoint is not None, f"endpoint {api_path} not found in parsed spec"

    # On-disk targets
    ondisk_cache_dir = CACHE_ROOT / "ontap" / Path(*module_parts)
    ondisk_models_dir = MODELS_ROOT / "ontap" / Path(*module_parts)
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
    seed_dir = temp_cache_dir / "ontap" / Path(*module_parts)
    seed_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ondisk_toml, seed_dir / f"{toml_stem}.toml")

    # Run the codegen pipeline into the temp tree.
    schema_lookup = {e.path: e.schema_name for e in parsed_endpoints}
    write_endpoint_files(
        endpoint,
        temp_cache_dir,
        "ontap",
        None,
        schema_lookup,
        models_dir=temp_models_dir,
    )

    generated_mapping = temp_cache_dir / "ontap" / Path(*module_parts) / "mapping.py"
    generated_model = temp_models_dir / "ontap" / Path(*module_parts) / "model.py"

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
