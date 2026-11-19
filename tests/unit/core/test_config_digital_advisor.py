"""Tests for the Digital Advisor settings model and loader (#1051)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from pynetappfoundry.core.config import SOPS_SETTING_TARGETS, Config, ConfigurationError
from pynetappfoundry.core.models import DigitalAdvisorAPISettings
from pynetappfoundry.utils.sops import SOPSError

DECRYPT = "pynetappfoundry.utils.sops.decrypt_value"
PAT = "placeholder-pat"
ACCESS = "placeholder-access-token"
REFRESH = "placeholder-refresh-token"


def _config(tmp_path: Path, general: str) -> Config:
    path = tmp_path / "cfg" / "apis" / "digitaladvisor" / "digitaladvisorapi.toml"
    path.parent.mkdir(parents=True)
    path.write_text(f"[general]\n{general}")
    return Config(config_dir=str(tmp_path / "cfg"), script_name="test")


@pytest.mark.parametrize(
    "fields",
    [
        {"personal_access_token": PAT},
        {"refresh_token": REFRESH},
        {"refresh_token": REFRESH, "access_token": ACCESS},
        {"personal_access_token": PAT, "refresh_token": REFRESH},
        {"personal_access_token": PAT, "refresh_token": REFRESH, "access_token": ACCESS},
    ],
)
def test_valid_credential_combinations(fields: dict[str, Any]) -> None:
    DigitalAdvisorAPISettings.model_validate(fields)


@pytest.mark.parametrize(
    "fields",
    [
        {},
        {"access_token": ACCESS},
        {"personal_access_token": PAT, "access_token": ACCESS},
    ],
)
def test_invalid_credential_combinations(fields: dict[str, Any]) -> None:
    with pytest.raises(ValidationError) as exc:
        DigitalAdvisorAPISettings.model_validate(fields)
    for value in (PAT, ACCESS, REFRESH):
        assert value not in str(exc.value)


def test_defaults() -> None:
    s = DigitalAdvisorAPISettings(personal_access_token=PAT)  # type: ignore[arg-type]
    assert s.graphql_url == "https://gql.aiq.netapp.com/graphql"
    assert s.token_url == "https://api.activeiq.netapp.com/v1/tokens/accessToken"
    assert s.timeout == 70.0
    assert s.page_size == 100
    assert s.uses_refresh_token is False


def test_page_size_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        DigitalAdvisorAPISettings.model_validate({"personal_access_token": PAT, "page_size": 0})


def test_loader_reads_plain_values(tmp_path: Path) -> None:
    config = _config(tmp_path, f'refresh_token = "{REFRESH}"\n')
    s = config.get_digital_advisor_api_settings()
    assert s.refresh_token is not None
    assert s.refresh_token.get_secret_value() == REFRESH
    assert s.uses_refresh_token is True


def test_loader_decrypts_sops_values(tmp_path: Path) -> None:
    config = _config(tmp_path, 'refresh_token = "SOPS[placeholder-cipher]"\n')
    with patch(DECRYPT, return_value=REFRESH):
        s = config.get_digital_advisor_api_settings()
    assert s.refresh_token is not None
    assert s.refresh_token.get_secret_value() == REFRESH


def test_loader_error_never_contains_values(tmp_path: Path) -> None:
    config = _config(tmp_path, f'personal_access_token = "{PAT}"\naccess_token = "{ACCESS}"\n')
    with pytest.raises(ConfigurationError) as exc:
        config.get_digital_advisor_api_settings()
    message = str(exc.value)
    assert PAT not in message
    assert ACCESS not in message
    assert "digitaladvisorapi.toml" in message


def test_decrypt_failure_never_contains_values(tmp_path: Path) -> None:
    config = _config(tmp_path, 'refresh_token = "SOPS[placeholder-cipher]"\n')
    with patch(DECRYPT, side_effect=SOPSError("detail")), pytest.raises(ConfigurationError) as exc:
        config.get_digital_advisor_api_settings()
    assert "placeholder-cipher" not in str(exc.value)


def test_missing_section_raises(tmp_path: Path) -> None:
    (tmp_path / "cfg").mkdir()
    config = Config(config_dir=str(tmp_path / "cfg"), script_name="test")
    with pytest.raises(ConfigurationError):
        config.get_digital_advisor_api_settings()


def test_set_credential_targets_exist() -> None:
    for field in ("personal_access_token", "access_token", "refresh_token"):
        assert SOPS_SETTING_TARGETS[f"digitaladvisorapi.{field}"] == (
            "digitaladvisorapi",
            "general",
            field,
        )


def test_loader_accepts_both_credentials(tmp_path: Path) -> None:
    config = _config(tmp_path, f'personal_access_token = "{PAT}"\nrefresh_token = "{REFRESH}"\n')
    s = config.get_digital_advisor_api_settings()
    assert s.personal_access_token is not None
    assert s.uses_refresh_token is True
