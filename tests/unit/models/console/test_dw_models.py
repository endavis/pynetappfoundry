"""Tests for the generated ``dw`` Console models (#1034)."""

from __future__ import annotations

import importlib
import pkgutil

from pynetappfoundry.models.console.dw import get_license_account_subscriptions_preferred as pref


def test_every_dw_module_imports() -> None:
    """Import all generated ``dw`` modules; also feeds the coverage gate."""
    package = importlib.import_module("pynetappfoundry.models.console.dw")
    names = [m.name for m in pkgutil.iter_modules(package.__path__)]
    assert len(names) > 0
    for name in names:
        importlib.import_module(f"{package.__name__}.{name}")


def test_preferred_response_validates_documented_example() -> None:
    body = pref.Response200Body.model_validate(
        {
            "accounts": ["account-placeholder"],
            "cloudProvider": "aws",
            "entitlements": {"items": [{"contractOption": "Professional", "usageReport": 12}]},
            "subscriptionId": "sub-placeholder-1",
            "endDate": 1556636730921,
            "term": "12 Months",
            "events": {"endDateEvent": {"type": "string", "subscriptionExpirationInDays": 3}},
        }
    )
    assert body.endDate == 1556636730921
    assert body.entitlements is not None
    assert body.entitlements.items is not None
    assert body.entitlements.items[0].contractOption == "Professional"


def test_preferred_response_accepts_null_nullable_fields() -> None:
    body = pref.Response200Body.model_validate(
        {"endDate": None, "term": None, "isPrivate": None, "listingUrl": None}
    )
    assert body.endDate is None
    assert body.isPrivate is None
