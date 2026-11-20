"""Tests for ``core/spec_source.py`` (#1129)."""

from __future__ import annotations

import json
from importlib import metadata
from unittest.mock import patch

import pytest

from pynetappfoundry.core import spec_source
from pynetappfoundry.core.spec_source import (
    ReleaseRef,
    SpecSourceError,
    github_repository,
    installed_repository,
    parse_spec,
    resolve_ref,
    spec_url,
)


def test_release_version_maps_to_tag() -> None:
    assert resolve_ref("1.2.3") == ReleaseRef("v1.2.3", dirty=False)


def test_dev_build_with_sha_uses_the_sha() -> None:
    assert resolve_ref("0.1.1.dev275+g1369c1b98") == ReleaseRef("1369c1b98", dirty=False)


def test_dirty_dev_build_is_flagged() -> None:
    assert resolve_ref("0.1.1.dev275+g1369c1b98.d20260101") == ReleaseRef("1369c1b98", dirty=True)


@pytest.mark.parametrize("version", ["0.1.1.dev3", "0.0.0", "0.1.1.dev3+local"])
def test_version_without_a_commit_raises_naming_the_version(version: str) -> None:
    with pytest.raises(SpecSourceError, match=version.replace("+", r"\+")) as info:
        resolve_ref(version)
    assert info.value.hint is not None
    assert "Spec files" in info.value.hint


def test_tag_prefix_matches_commitizen_tag_format() -> None:
    import tomllib
    from pathlib import Path

    root = Path(spec_source.__file__).resolve().parents[3]
    data = tomllib.loads((root / "pyproject.toml").read_text())
    assert data["tool"]["commitizen"]["tag_format"] == f"{spec_source.TAG_PREFIX}$version"


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/example-owner/example-repo",
        "https://github.com/example-owner/example-repo.git",
        "https://github.com/example-owner/example-repo/",
    ],
)
def test_github_repository_parses_url_forms(url: str) -> None:
    assert github_repository([f"Repository, {url}"]) == ("example-owner", "example-repo")


@pytest.mark.parametrize(
    "urls",
    [
        None,
        [],
        ["Homepage, https://github.com/example-owner/example-repo"],
        ["Repository, https://gitlab.com/example-owner/example-repo"],
        ["Repository, https://github.com/example-owner"],
    ],
)
def test_github_repository_rejects_missing_or_foreign(urls: list[str] | None) -> None:
    with pytest.raises(SpecSourceError):
        github_repository(urls)


def test_installed_repository_converts_package_not_found() -> None:
    with (
        patch.object(spec_source.metadata, "metadata", side_effect=metadata.PackageNotFoundError),
        pytest.raises(SpecSourceError, match="not installed"),
    ):
        installed_repository()


def test_spec_url_composes_raw_url() -> None:
    assert spec_url("example-owner", "example-repo", "v1.0.0", "docs/a.json") == (
        "https://raw.githubusercontent.com/example-owner/example-repo/v1.0.0/docs/a.json"
    )


def test_parse_spec_accepts_json_and_yaml() -> None:
    assert parse_spec(json.dumps({"paths": {}}), "all.json") == {"paths": {}}
    assert parse_spec("paths:\n  /a: {}\n", "x.yaml") == {"paths": {"/a": {}}}


@pytest.mark.parametrize(
    ("text", "name"),
    [
        ("{not json", "all.json"),
        ("a: [", "x.yaml"),
        ("[1, 2]", "all.json"),
        ("{}", "all.json"),
        ('{"paths": []}', "all.json"),
        ("- a\n", "x.yaml"),
    ],
)
def test_parse_spec_rejects_unusable_text(text: str, name: str) -> None:
    with pytest.raises(SpecSourceError):
        parse_spec(text, name)
