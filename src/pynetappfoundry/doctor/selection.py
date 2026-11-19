"""Select the ``nf doctor`` check rows that belong to the APIs named by ``--api`` (ADR-0035).

The tags live here, not in ``core.config_checks``, so ``nf config validate`` is unchanged.
Static rows are classified by their ``subject`` (the stable key of a result, ADR-0034);
SOPS values are classified from the config structure while they are collected.

The module is pure: it imports no Rich, click, client or cache module.
"""

from __future__ import annotations

from collections.abc import Collection, Iterable, Mapping

from pynetappfoundry.core.config_checks import CheckResult, CheckSection
from pynetappfoundry.doctor import API_NAMES

DATA_TYPE_APIS: Mapping[str, str] = {
    "clusters": "ontap",
    "aiqums": "aiqum",
    "cloudinsights": "dii",
    "connectors": "console",
}
"""Data object type to the API that reads it. ``azure`` and ``ibm`` belong to none."""

SETTINGS_APIS: Mapping[str, str] = {
    "ontapapi": "ontap",
    "aiqumapi": "aiqum",
    "diiapi": "dii",
    "consoleapi": "console",
    "digitaladvisorapi": "digitaladvisor",
}
"""Settings stem to the API it configures."""

USER_TYPE_APIS: Mapping[str, str] = {**DATA_TYPE_APIS, "console": "console"}
"""``users.<type>`` to the API that uses those accounts."""

ALL_USER_APIS: frozenset[str] = frozenset({"ontap", "aiqum", "dii", "console"})
"""Every API that reads ``users.toml``; Digital Advisor does not."""

_GLOBAL_SUBJECTS: frozenset[str] = frozenset({"settings", "licensing", "monitoring"})


def apis_for_subject(subject: str) -> frozenset[str] | None:
    """Return the APIs a static check subject belongs to.

    Returns:
        The APIs (empty for a global setting no API depends on), or None when the
        subject is not recognised, so the row is kept rather than hidden.
    """
    head, _, rest = subject.partition(".")
    if head in _GLOBAL_SUBJECTS:
        return frozenset()
    if head == "users":
        if not rest:
            return ALL_USER_APIS
        api = USER_TYPE_APIS.get(rest.partition(".")[0])
        return frozenset({api}) if api else frozenset()
    if head == "spec":
        return frozenset({rest}) if rest in API_NAMES else frozenset()
    api = DATA_TYPE_APIS.get(head) or SETTINGS_APIS.get(head)
    if api:
        return frozenset({api})
    return None


def select_results(
    results: Iterable[CheckResult], apis: Collection[str]
) -> tuple[CheckResult, ...]:
    """Keep the results that belong to one of ``apis`` or that are not classified."""
    wanted = set(apis)
    kept: list[CheckResult] = []
    for result in results:
        owners = apis_for_subject(result.subject)
        if owners is None or owners & wanted:
            kept.append(result)
    return tuple(kept)


def select_sections(
    sections: list[CheckSection], apis: Collection[str] | None
) -> list[CheckSection]:
    """Filter static sections to ``apis``, dropping sections left empty.

    ``None`` means no ``--api`` was given and returns ``sections`` unchanged.
    """
    if apis is None:
        return sections
    selected: list[CheckSection] = []
    for section in sections:
        results = select_results(section.results, apis)
        if results:
            selected.append(CheckSection(section.title, results))
    return selected
