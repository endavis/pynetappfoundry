"""Walk a service folder and run the endpoint parser against every ``.adoc`` file."""

from __future__ import annotations

from pathlib import Path

from tools.console_openapi.models import (
    ParsedEndpoint,
    ParseError,
    ParseReport,
)
from tools.console_openapi.parser.endpoint import (
    EndpointParseError,
    parse_endpoint,
)


def parse_service(repo_root: Path, service: str, *, strict: bool = True) -> ParseReport:
    """Parse every ``.adoc`` file under ``repo_root/service``.

    In ``strict=True`` mode, a parse error raises :class:`EndpointParseError`.
    In ``strict=False`` mode (lenient), errors are recorded in the returned
    report and parsing continues with the next file.
    """
    service_dir = repo_root / service
    if not service_dir.is_dir():
        raise FileNotFoundError(f"Service folder not found: {service_dir}")

    endpoints: list[ParsedEndpoint] = []
    skipped: list[str] = []
    errors: list[ParseError] = []

    for adoc in sorted(service_dir.glob("*.adoc")):
        rel = adoc.relative_to(repo_root).as_posix()
        try:
            text = adoc.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            if strict:
                raise EndpointParseError(f"Cannot read {rel}: {exc}") from exc
            errors.append(ParseError(source_file=rel, section="read", message=str(exc)))
            continue

        try:
            ep = parse_endpoint(text, source_file=rel, service=service)
        except Exception as exc:
            if strict:
                raise EndpointParseError(f"Failed to parse {rel}: {exc}") from exc
            errors.append(ParseError(source_file=rel, section="endpoint", message=str(exc)))
            continue

        if ep is None:
            skipped.append(rel)
        else:
            endpoints.append(ep)

    return ParseReport(
        endpoints=tuple(endpoints),
        skipped_overview=tuple(skipped),
        errors=tuple(errors),
    )
