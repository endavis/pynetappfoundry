"""Tests for the send_email utility."""

from __future__ import annotations

import email
import logging
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import SecretStr

from pynetappfoundry.core.models import SMTPSettings
from pynetappfoundry.utils.email import send_email


def _config(**overrides: Any) -> MagicMock:
    """Build a Config stand-in whose get_smtp_settings returns real SMTPSettings."""
    values: dict[str, Any] = {"server": "smtp.example.com", **overrides}
    config = MagicMock()
    config.get_smtp_settings.return_value = SMTPSettings(**values)
    return config


def _sent_message(server: MagicMock) -> email.message.Message:
    """Parse the message string passed to sendmail."""
    return email.message_from_string(server.sendmail.call_args.args[2])


def _parts(msg: email.message.Message) -> list[email.message.Message]:
    """Return the sub-parts of a multipart message."""
    return list(msg.iter_parts()) if hasattr(msg, "iter_parts") else list(msg.walk())[1:]


def _text(part: email.message.Message) -> str:
    """Decode a text part's payload."""
    payload = part.get_payload(decode=True)
    assert isinstance(payload, bytes)
    return payload.decode()


@pytest.fixture
def smtp() -> Any:
    """Patch smtplib.SMTP and yield (class mock, server mock)."""
    with patch("pynetappfoundry.utils.email.smtplib.SMTP") as smtp_cls:
        yield smtp_cls, smtp_cls.return_value


class TestSendEmailConnection:
    """Connection, auth and envelope behavior."""

    def test_connects_with_host_and_port(self, smtp: Any) -> None:
        """SMTP is opened with the configured server and port."""
        smtp_cls, _ = smtp
        send_email(_config(port=2525), mailto="to@x.com", mailfrom="from@x.com")
        smtp_cls.assert_called_once_with("smtp.example.com", 2525)

    def test_default_port(self, smtp: Any) -> None:
        """Port defaults to 25."""
        smtp_cls, _ = smtp
        send_email(_config(), mailto="to@x.com", mailfrom="from@x.com")
        smtp_cls.assert_called_once_with("smtp.example.com", 25)

    def test_no_login_when_auth_false(self, smtp: Any) -> None:
        """login is not called when auth is not 'True'."""
        _, server = smtp
        send_email(_config(auth="False"), mailto="to@x.com", mailfrom="from@x.com")
        server.login.assert_not_called()

    def test_login_when_auth_true(self, smtp: Any) -> None:
        """login receives the user and the unwrapped password."""
        _, server = smtp
        cfg = _config(auth="True", user="bob", password=SecretStr("s3cret"))
        send_email(cfg, mailto="to@x.com", mailfrom="from@x.com")
        server.login.assert_called_once_with("bob", "s3cret")

    def test_login_happens_before_sendmail(self, smtp: Any) -> None:
        """Authentication precedes sending, and quit comes last."""
        _, server = smtp
        cfg = _config(auth="True", user="bob", password=SecretStr("pw"))
        send_email(cfg, mailto="to@x.com", mailfrom="from@x.com")
        names = [c[0] for c in server.method_calls]
        assert names == ["login", "sendmail", "quit"]

    def test_sendmail_envelope(self, smtp: Any) -> None:
        """sendmail gets the sender and recipient as the envelope."""
        _, server = smtp
        send_email(_config(), mailto="to@x.com", mailfrom="from@x.com")
        args = server.sendmail.call_args.args
        assert args[0] == "from@x.com"
        assert args[1] == "to@x.com"
        server.quit.assert_called_once_with()


class TestSendEmailMessage:
    """Headers and body of the built message."""

    def test_headers_and_plain_body(self, smtp: Any) -> None:
        """From, To, Subject and a plain-text body are set."""
        _, server = smtp
        send_email(
            _config(),
            subject="Hello",
            body="Body text",
            mailto="to@x.com",
            mailfrom="from@x.com",
        )
        msg = _sent_message(server)
        assert msg["From"] == "from@x.com"
        assert msg["To"] == "to@x.com"
        assert msg["Subject"] == "Hello"
        assert msg.is_multipart()
        parts = _parts(msg)
        assert len(parts) == 1
        assert parts[0].get_content_type() == "text/plain"
        assert _text(parts[0]) == "Body text"

    def test_html_body_type(self, smtp: Any) -> None:
        """body_type='html' yields a text/html part."""
        _, server = smtp
        send_email(
            _config(),
            body="<b>hi</b>",
            body_type="html",
            mailto="to@x.com",
            mailfrom="from@x.com",
        )
        part = _parts(_sent_message(server))[0]
        assert part.get_content_type() == "text/html"
        assert _text(part) == "<b>hi</b>"

    def test_default_subject_and_body_are_empty(self, smtp: Any) -> None:
        """Omitted subject and body are empty strings."""
        _, server = smtp
        send_email(_config(), mailto="to@x.com", mailfrom="from@x.com")
        msg = _sent_message(server)
        assert msg["Subject"] == ""
        assert _text(_parts(msg)[0]) == ""

    def test_high_priority_headers(self, smtp: Any) -> None:
        """high_priority adds both priority headers."""
        _, server = smtp
        send_email(_config(), mailto="to@x.com", mailfrom="from@x.com", high_priority=True)
        msg = _sent_message(server)
        assert msg["X-Priority"] == "1"
        assert msg["X-MSMail-Priority"] == "High"

    def test_normal_priority_has_no_priority_headers(self, smtp: Any) -> None:
        """Without high_priority no priority headers are present."""
        _, server = smtp
        send_email(_config(), mailto="to@x.com", mailfrom="from@x.com")
        msg = _sent_message(server)
        assert msg["X-Priority"] is None
        assert msg["X-MSMail-Priority"] is None


class TestSendEmailErrors:
    """Error paths."""

    @pytest.mark.parametrize(
        ("mailto", "mailfrom", "fragment"),
        [
            (None, "from@x.com", "No To Email address specified"),
            ("", "from@x.com", "No To Email address specified"),
            ("to@x.com", None, "No From Email address specified"),
            ("to@x.com", "", "No From Email address specified"),
        ],
    )
    def test_missing_address_logs_and_skips_smtp(
        self,
        smtp: Any,
        caplog: pytest.LogCaptureFixture,
        mailto: str | None,
        mailfrom: str | None,
        fragment: str,
    ) -> None:
        """A missing address logs an error naming the file and never opens SMTP."""
        smtp_cls, _ = smtp
        with caplog.at_level(logging.ERROR):
            send_email(_config(), mailto=mailto, mailfrom=mailfrom)
        smtp_cls.assert_not_called()
        assert f"email.py : {fragment}" in caplog.text

    def test_both_missing_reports_to_first(
        self, smtp: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        """With both addresses missing, only the To error is logged."""
        with caplog.at_level(logging.ERROR):
            send_email(_config())
        assert "No To Email address" in caplog.text
        assert "No From Email address" not in caplog.text

    def test_connection_failure_is_logged_not_raised(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """An SMTP connection error is logged with the server and message."""
        with (
            patch("pynetappfoundry.utils.email.smtplib.SMTP", side_effect=OSError("refused")),
            caplog.at_level(logging.ERROR),
        ):
            send_email(_config(), mailto="to@x.com", mailfrom="from@x.com")
        assert "email.py : Failed to send email: smtp.example.com refused" in caplog.text

    def test_login_failure_is_logged_and_skips_send(
        self, smtp: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A login error is logged and nothing is sent."""
        _, server = smtp
        server.login.side_effect = RuntimeError("bad creds")
        cfg = _config(auth="True", user="bob", password=SecretStr("pw"))
        with caplog.at_level(logging.ERROR):
            send_email(cfg, mailto="to@x.com", mailfrom="from@x.com")
        server.sendmail.assert_not_called()
        assert "Failed to send email: smtp.example.com bad creds" in caplog.text

    def test_sendmail_failure_is_logged(self, smtp: Any, caplog: pytest.LogCaptureFixture) -> None:
        """A sendmail error is logged, not raised."""
        _, server = smtp
        server.sendmail.side_effect = RuntimeError("rejected")
        with caplog.at_level(logging.ERROR):
            send_email(_config(), mailto="to@x.com", mailfrom="from@x.com")
        assert "Failed to send email: smtp.example.com rejected" in caplog.text


class TestSendEmailWireFormat:
    """Header names and content type as written on the wire (case-sensitive)."""

    def test_header_names_exact_case(self, smtp: Any) -> None:
        """Standard headers are emitted with their canonical capitalisation."""
        _, server = smtp
        send_email(
            _config(),
            subject="Hello",
            mailto="to@x.com",
            mailfrom="from@x.com",
            high_priority=True,
        )
        lines = server.sendmail.call_args.args[2].splitlines()
        assert "From: from@x.com" in lines
        assert "To: to@x.com" in lines
        assert "Subject: Hello" in lines
        assert "X-Priority: 1" in lines
        assert "X-MSMail-Priority: High" in lines

    def test_default_body_type_is_lowercase_plain(self, smtp: Any) -> None:
        """The default body type is written as text/plain."""
        _, server = smtp
        send_email(_config(), body="x", mailto="to@x.com", mailfrom="from@x.com")
        assert 'Content-Type: text/plain; charset="us-ascii"' in server.sendmail.call_args.args[2]
