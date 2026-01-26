"""Email utility functions."""

from __future__ import annotations

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

_file_name = Path(__file__).name


def send_email(
    config: Config,
    subject: str = "",
    body: str = "",
    body_type: str = "plain",
    mailto: str | None = None,
    mailfrom: str | None = None,
    high_priority: bool = False,
) -> None:
    """Send an email using SMTP settings from config.

    Args:
        config: Configuration object with SMTP settings.
        subject: Email subject.
        body: Email body content.
        body_type: MIME type of body ('plain' or 'html').
        mailto: Recipient email address.
        mailfrom: Sender email address.
        high_priority: If True, mark email as high priority.
    """
    # Email configuration
    smtp_server = config.settings["settings"]["SMTP"]["server"]
    smtp_port = int(config.settings["settings"]["SMTP"]["port"])
    smtp_user = config.settings["settings"]["SMTP"]["user"]
    smtp_password = config.settings["settings"]["SMTP"]["password"]
    auth = config.settings["settings"]["SMTP"]["auth"]

    if not mailto:
        logging.error(f"{_file_name} : No To Email address specified")
        return
    if not mailfrom:
        logging.error(f"{_file_name} : No From Email address specified")
        return

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = mailfrom
    msg["To"] = mailto
    msg["Subject"] = subject
    if high_priority:
        msg["X-Priority"] = "1"  # High priority
        msg["X-MSMail-Priority"] = "High"  # High priority for MS Outlook
    msg.attach(MIMEText(body, body_type))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        if auth == "True":
            server.login(smtp_user, smtp_password)
        server.sendmail(mailfrom, mailto, msg.as_string())
        server.quit()
    except Exception as e:
        logging.error(f"{_file_name} : Failed to send email: {smtp_server} {e}")
