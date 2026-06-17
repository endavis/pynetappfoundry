"""Tests for the matcher helpers in ``cli.commands.cifs.session``."""

from __future__ import annotations

import click
import pytest

from pynetappfoundry.cli.commands.cifs.session import (
    _has_glob,
    _is_cidr,
    _is_plain_ip,
    _matches_ip,
    _matches_user,
    _validate_ip_pattern,
)


class TestMatchesUser:
    def test_substring_default_case_insensitive(self) -> None:
        assert _matches_user("DOMAIN\\JDoe", "", "jdoe", case_sensitive=False)

    def test_substring_case_sensitive_no_match(self) -> None:
        assert not _matches_user("DOMAIN\\JDoe", "", "jdoe", case_sensitive=True)

    def test_substring_case_sensitive_match(self) -> None:
        assert _matches_user("DOMAIN\\jdoe", "", "jdoe", case_sensitive=True)

    def test_glob_star(self) -> None:
        assert _matches_user("DOMAIN\\jdoe", "", "*jdoe*", case_sensitive=False)

    def test_glob_question_mark(self) -> None:
        assert _matches_user("jdoe", "", "?doe", case_sensitive=False)

    def test_glob_no_match(self) -> None:
        assert not _matches_user("alice", "", "*jdoe*", case_sensitive=False)

    def test_mapped_unix_user_fallback(self) -> None:
        assert _matches_user("", "jdoe", "jdoe", case_sensitive=False)

    def test_mapped_unix_user_glob(self) -> None:
        assert _matches_user("", "jdoe", "*doe*", case_sensitive=False)

    def test_empty_pattern_returns_false(self) -> None:
        assert not _matches_user("jdoe", "jdoe", "", case_sensitive=False)

    def test_both_empty_haystack_no_match(self) -> None:
        assert not _matches_user("", "", "jdoe", case_sensitive=False)

    def test_glob_case_sensitive_no_match(self) -> None:
        assert not _matches_user("JDOE", "", "*jdoe*", case_sensitive=True)

    def test_backslash_literal_substring(self) -> None:
        # Plain (non-glob) pattern with backslash should substring-match.
        assert _matches_user("DOMAIN\\jdoe", "", "DOMAIN\\jdoe", case_sensitive=False)


class TestMatchesIp:
    def test_exact_v4(self) -> None:
        assert _matches_ip("10.1.2.45", "10.1.2.45")

    def test_exact_v4_normalized(self) -> None:
        # 010.001.002.045 → not valid; use canonical form only.
        assert not _matches_ip("10.1.2.45", "10.1.2.46")

    def test_glob_v4(self) -> None:
        assert _matches_ip("10.1.2.45", "10.1.2.*")
        assert not _matches_ip("10.1.3.45", "10.1.2.*")

    def test_cidr_v4(self) -> None:
        assert _matches_ip("10.1.2.45", "10.1.2.0/24")
        assert not _matches_ip("10.1.3.45", "10.1.2.0/24")

    def test_cidr_v6(self) -> None:
        assert _matches_ip("2001:db8::1", "2001:db8::/32")

    def test_cidr_address_family_mismatch(self) -> None:
        assert not _matches_ip("2001:db8::1", "10.1.2.0/24")
        assert not _matches_ip("10.1.2.45", "2001:db8::/32")

    def test_cidr_invalid_returns_false(self) -> None:
        # _matches_ip never raises; invalid input returns False.
        assert not _matches_ip("not-an-ip", "10.1.2.0/24")

    def test_empty_pattern_or_ip(self) -> None:
        assert not _matches_ip("", "10.1.2.45")
        assert not _matches_ip("10.1.2.45", "")


class TestValidateIpPattern:
    def test_plain_ip_ok(self) -> None:
        _validate_ip_pattern("10.1.2.45")

    def test_cidr_ok(self) -> None:
        _validate_ip_pattern("10.1.2.0/24")

    def test_glob_ok(self) -> None:
        _validate_ip_pattern("10.1.2.*")

    def test_invalid_raises(self) -> None:
        with pytest.raises(click.BadParameter):
            _validate_ip_pattern("not-an-ip")

    def test_invalid_cidr_raises(self) -> None:
        with pytest.raises(click.BadParameter):
            _validate_ip_pattern("10.1.2.0/99")

    def test_empty_raises(self) -> None:
        with pytest.raises(click.BadParameter):
            _validate_ip_pattern("")


class TestHelpers:
    def test_has_glob(self) -> None:
        assert _has_glob("*jdoe*")
        assert _has_glob("j?oe")
        assert _has_glob("j[oa]e")
        assert not _has_glob("jdoe")
        assert not _has_glob("DOMAIN\\jdoe")

    def test_is_plain_ip(self) -> None:
        assert _is_plain_ip("10.1.2.45")
        assert _is_plain_ip("2001:db8::1")
        assert not _is_plain_ip("10.1.2.0/24")
        assert not _is_plain_ip("10.1.2.*")
        assert not _is_plain_ip("")

    def test_is_cidr(self) -> None:
        assert _is_cidr("10.1.2.0/24")
        assert _is_cidr("2001:db8::/32")
        assert not _is_cidr("10.1.2.45")
        assert not _is_cidr("10.1.2.*")
