"""Tests for the compact ``AccountSubscription`` type (#1034)."""

from __future__ import annotations

import pydantic
import pytest

from pynetappfoundry.models.console.dw import get_license_account_subscriptions_preferred as dw
from pynetappfoundry.models.console_types import AccountSubscription, SubscriptionEntitlement


def _body(**kwargs: object) -> dw.Response200Body:
    return dw.Response200Body.model_validate(kwargs)


class TestAccountSubscription:
    def test_parses_camel_case_and_snake_case(self) -> None:
        camel = AccountSubscription.model_validate({"subscriptionId": "s1", "endDate": 5})
        snake = AccountSubscription.model_validate({"subscription_id": "s1", "end_date": 5})
        assert camel == snake
        assert camel.end_date == 5

    def test_round_trips_by_alias(self) -> None:
        sub = AccountSubscription.model_validate(
            {"subscriptionId": "s1", "entitlements": [{"contractOption": "Pro"}]}
        )
        dumped = sub.model_dump(by_alias=True)
        assert dumped["subscriptionId"] == "s1"
        assert dumped["entitlements"][0]["contractOption"] == "Pro"
        assert AccountSubscription.model_validate(dumped) == sub

    def test_missing_subscription_id_raises(self) -> None:
        with pytest.raises(pydantic.ValidationError):
            AccountSubscription.model_validate({"subscriptionName": "no-id"})

    def test_from_preferred_maps_entitlements_and_drops_fields(self) -> None:
        body = _body(
            subscriptionId="sub-placeholder-1",
            subscriptionStatus="subscribed",
            endDate=1556636730921,
            term="12 Months",
            accounts=["account-placeholder"],
            customerIdentifier="customer-placeholder",
            cloudIds=["cloud-placeholder"],
            listingUrl="https://example.invalid/listing",
            entitlements={
                "items": [{"contractOption": "Professional", "units": "12 TiB", "unit": "TiB"}]
            },
        )
        sub = AccountSubscription.from_preferred(body)
        assert sub.subscription_id == "sub-placeholder-1"
        assert sub.end_date == 1556636730921
        assert sub.accounts == ["account-placeholder"]
        assert sub.entitlements == [
            SubscriptionEntitlement.model_validate(
                {"contract_option": "Professional", "units": "12 TiB", "unit": "TiB"}
            )
        ]
        dumped = sub.model_dump_json()
        for dropped in ("customer-placeholder", "cloud-placeholder", "listing"):
            assert dropped not in dumped

    def test_from_preferred_null_entitlements_and_items(self) -> None:
        assert AccountSubscription.from_preferred(_body(subscriptionId="s")).entitlements == []
        body = _body(subscriptionId="s", entitlements={"items": None}, accounts=None)
        sub = AccountSubscription.from_preferred(body)
        assert sub.entitlements == []
        assert sub.accounts == []

    def test_from_preferred_without_subscription_id_raises(self) -> None:
        with pytest.raises(pydantic.ValidationError):
            AccountSubscription.from_preferred(_body())

    def test_in_all(self) -> None:
        from pynetappfoundry.models import console_types

        assert "AccountSubscription" in console_types.__all__
        assert "SubscriptionEntitlement" in console_types.__all__
