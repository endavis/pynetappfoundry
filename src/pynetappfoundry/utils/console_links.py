"""Build URLs that open NetApp Console (BlueXP) objects in the UI.

Pure functions, no I/O.  The on-prem vs Cloud Volumes ONTAP (CVO) split comes
from the working environment ``publicId`` prefix, since ``workingEnvironmentType``
has no enum in the spec.  Links that are not direct say so in their docstrings.
"""

from __future__ import annotations

from urllib.parse import quote

CONSOLE_UI_BASE_URL = "https://console.netapp.com"

ONPREM_PREFIX = "OnPremWorkingEnvironment-"
CVO_PREFIX = "VsaWorkingEnvironment-"

_WE_PATHS: dict[str, str] = {
    ONPREM_PREFIX: "storage/on-prem",
    CVO_PREFIX: "storage/cloud-volumes-ontap",
}


def _base(base_url: str) -> str:
    """Return ``base_url`` without a trailing slash."""
    return base_url.rstrip("/")


def _we_path(public_id: str) -> str:
    """Return the UI path segment for a working environment ``publicId``.

    Raises:
        ValueError: If ``public_id`` is empty or has an unknown prefix.
    """
    if not public_id:
        raise ValueError("Working environment publicId must not be empty")
    for prefix, path in _WE_PATHS.items():
        if public_id.startswith(prefix):
            return path
    raise ValueError(
        f"Unknown working environment publicId prefix: {public_id!r} "
        f"(expected {ONPREM_PREFIX!r} or {CVO_PREFIX!r})"
    )


def is_cvo_public_id(public_id: str) -> bool:
    """Return True when ``public_id`` is a Cloud Volumes ONTAP working environment."""
    return public_id.startswith(CVO_PREFIX)


def build_console_working_environment_link(
    public_id: str, *, base_url: str = CONSOLE_UI_BASE_URL
) -> str:
    """Build the URL of a working environment page.

    Raises:
        ValueError: If ``public_id`` is empty or has an unknown prefix.
    """
    path = _we_path(public_id)
    return f"{_base(base_url)}/{path}/{quote(public_id, safe='')}"


def build_console_volumes_link(public_id: str, *, base_url: str = CONSOLE_UI_BASE_URL) -> str:
    """Build the URL of a working environment's Volumes tab.

    Not a direct link to a single volume: the Console opens the working
    environment's Volumes tab (``<working environment URL>/volumes``).

    Raises:
        ValueError: If ``public_id`` is empty or has an unknown prefix.
    """
    return f"{build_console_working_environment_link(public_id, base_url=base_url)}/volumes"


def build_console_svm_link(public_id: str, *, base_url: str = CONSOLE_UI_BASE_URL) -> str:
    """Build the URL for an SVM.

    Not a direct link: the Console has no per-SVM page, so this is the
    working environment's URL.

    Raises:
        ValueError: If ``public_id`` is empty or has an unknown prefix.
    """
    return build_console_working_environment_link(public_id, base_url=base_url)


def build_console_aggregates_link(public_id: str, *, base_url: str = CONSOLE_UI_BASE_URL) -> str:
    """Build the URL of a CVO working environment's Aggregates view.

    Raises:
        ValueError: If ``public_id`` is empty, has an unknown prefix, or is an
            on-prem working environment (on-prem has no aggregates view).
    """
    if not is_cvo_public_id(public_id):
        _we_path(public_id)  # validates empty and unknown prefixes first
        raise ValueError(f"Aggregates links exist only for CVO working environments: {public_id!r}")
    return f"{build_console_working_environment_link(public_id, base_url=base_url)}/aggregates"


def build_console_agents_link(*, base_url: str = CONSOLE_UI_BASE_URL) -> str:
    """Build the URL of the Console agents list."""
    return f"{_base(base_url)}/agents-mgmt"


def build_console_agent_edit_link(agent_id: str, *, base_url: str = CONSOLE_UI_BASE_URL) -> str:
    """Build the URL of a Console agent's edit page.

    The Console has no agent detail page, so the edit page is the link target.

    Raises:
        ValueError: If ``agent_id`` is empty.
    """
    if not agent_id:
        raise ValueError("agent_id must not be empty")
    return f"{build_console_agents_link(base_url=base_url)}/{quote(agent_id, safe='')}/edit"
