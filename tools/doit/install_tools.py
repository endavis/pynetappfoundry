"""Reusable framework for installing tools from GitHub releases.

Also provides SOPS credential encryption tool tasks:
- age: Encryption tool for SOPS
- sops: Secrets management
"""

import json
import os
import platform
import shutil
import subprocess  # nosec B404 - subprocess is required for version checks
import sys
import urllib.request
from pathlib import Path
from typing import Any

from doit.tools import title_with_actions


def get_latest_github_release(repo: str) -> str:
    """Get the latest release version for a GitHub repository.

    Queries the GitHub API for the latest release tag. Supports
    authenticated requests via GITHUB_TOKEN environment variable.

    Args:
        repo: GitHub repository in "owner/name" format (e.g. "direnv/direnv").

    Returns:
        Version string with leading 'v' stripped (e.g. "2.34.0").
    """
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    request = urllib.request.Request(url)

    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        request.add_header("Authorization", f"token {github_token}")

    with urllib.request.urlopen(request) as response:  # nosec B310 - URL is hardcoded GitHub API
        data = json.loads(response.read().decode())
        tag_name: str = data["tag_name"]
        return tag_name.lstrip("v")


def get_install_dir() -> Path:
    """Get the standard installation directory for user-local binaries.

    Returns:
        Path to ~/.local/bin, created if it does not exist.
    """
    install_dir = Path.home() / ".local" / "bin"
    install_dir.mkdir(parents=True, exist_ok=True)
    return install_dir


def download_github_release_binary(
    repo: str, version: str, asset_pattern: str, dest_name: str
) -> Path:
    """Download a binary asset from a GitHub release.

    Constructs the download URL from the repo, version, and asset pattern,
    downloads the file to the user-local bin directory, and makes it
    executable.

    Args:
        repo: GitHub repository in "owner/name" format.
        version: Release version (without leading 'v').
        asset_pattern: Filename pattern with {version} placeholder
            (e.g. "tool.linux-amd64" or "tool-v{version}-linux-amd64").
        dest_name: Name of the installed binary (e.g. "tool").

    Returns:
        Path to the downloaded and installed binary.
    """
    asset_name = asset_pattern.format(version=version)
    url = f"https://github.com/{repo}/releases/download/v{version}/{asset_name}"
    install_dir = get_install_dir()
    dest_path = install_dir / dest_name

    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, dest_path)  # nosec B310 - downloading from constructed GitHub release URL
    dest_path.chmod(0o755)  # nosec B103 - rwxr-xr-x is required for executable binary

    return dest_path


def install_tool(
    name: str,
    repo: str,
    asset_patterns: dict[str, str],
    version_cmd: list[str] | None = None,
    post_install_message: str | None = None,
) -> None:
    """Install a tool from GitHub releases if not already present.

    Checks if the tool is already on PATH. If so, prints its version
    and returns. Otherwise, downloads the latest release for the current
    platform and installs it.

    Args:
        name: Tool name used for PATH lookup and as the binary dest name.
        repo: GitHub repository in "owner/name" format.
        asset_patterns: Mapping of platform.system().lower() values
            (e.g. "linux", "darwin") to asset filename patterns.
            Patterns may include a {version} placeholder.
        version_cmd: Command list to run for checking installed version
            (e.g. ["tool", "--version"]). Defaults to [name, "--version"].
        post_install_message: Optional message printed after installation.
    """
    if version_cmd is None:
        version_cmd = [name, "--version"]

    if shutil.which(name):
        result = subprocess.run(
            version_cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        version_output = result.stdout.strip() or result.stderr.strip()
        print(f"OK: {name} already installed: {version_output}")
        return

    print(f"Installing {name}...")
    version = get_latest_github_release(repo)
    print(f"Latest version: {version}")

    system = platform.system().lower()
    if system == "darwin":
        subprocess.run(["brew", "install", name], check=True)
    elif system in asset_patterns:
        download_github_release_binary(
            repo=repo,
            version=version,
            asset_pattern=asset_patterns[system],
            dest_name=name,
        )
    else:
        print(f"Unsupported OS for {name}: {system}")
        sys.exit(1)

    print(f"OK: {name} installed.")
    if post_install_message:
        print(post_install_message)


def create_install_task(
    name: str,
    repo: str,
    asset_patterns: dict[str, str],
    version_cmd: list[str] | None = None,
    post_install_message: str | None = None,
) -> dict[str, Any]:
    """Create a doit task dict for installing a tool from GitHub releases.

    This is a factory function that returns a doit-compatible task
    dictionary. The task's action calls install_tool with the provided
    parameters.

    Args:
        name: Tool name used for PATH lookup and as the binary dest name.
        repo: GitHub repository in "owner/name" format.
        asset_patterns: Mapping of platform names to asset filename patterns.
        version_cmd: Command list for version check. Defaults to [name, "--version"].
        post_install_message: Optional message printed after installation.

    Returns:
        A doit task dictionary with actions and title.
    """

    def _action() -> None:
        install_tool(
            name=name,
            repo=repo,
            asset_patterns=asset_patterns,
            version_cmd=version_cmd,
            post_install_message=post_install_message,
        )

    return {
        "actions": [_action],
        "title": title_with_actions,
    }


# --- SOPS credential encryption tools ---


def _install_age() -> None:
    """Install age encryption tool.

    Age requires special handling because the Linux release is a tarball
    containing multiple binaries (age + age-keygen), not a single binary.
    """
    if shutil.which("age"):
        result = subprocess.run(
            ["age", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        version_output = result.stdout.strip() or result.stderr.strip()
        print(f"OK: age already installed: {version_output}")
        return

    print("Installing age...")
    version = get_latest_github_release("FiloSottile/age")
    print(f"Latest version: {version}")

    system = platform.system().lower()
    install_dir = get_install_dir()

    if system == "linux":
        tar_url = f"https://github.com/FiloSottile/age/releases/download/v{version}/age-v{version}-linux-amd64.tar.gz"
        tar_path = Path("/tmp/age.tar.gz")  # nosec B108
        print(f"Downloading {tar_url}...")
        urllib.request.urlretrieve(tar_url, tar_path)  # nosec B310

        import tarfile

        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall("/tmp")  # nosec B202 B108

        for binary in ["age", "age-keygen"]:
            src = Path("/tmp/age") / binary
            dst = install_dir / binary
            shutil.move(str(src), str(dst))
            dst.chmod(0o755)  # nosec B103

        tar_path.unlink()
        shutil.rmtree("/tmp/age", ignore_errors=True)
    elif system == "darwin":
        subprocess.run(["brew", "install", "age"], check=True)
    elif system == "windows":
        import glob
        import zipfile

        zip_url = f"https://github.com/FiloSottile/age/releases/download/v{version}/age-v{version}-windows-amd64.zip"
        zip_path = Path(os.environ.get("TEMP", ".")) / "age.zip"
        extract_dir = Path(os.environ.get("TEMP", ".")) / "age_extract"
        print(f"Downloading {zip_url}...")
        urllib.request.urlretrieve(zip_url, zip_path)  # nosec B310

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)  # nosec B202

        for exe in ["age.exe", "age-keygen.exe"]:
            matches = glob.glob(str(extract_dir / "**" / exe), recursive=True)
            if matches:
                shutil.move(matches[0], str(install_dir / exe))
            else:
                print(f"Warning: {exe} not found in archive")

        zip_path.unlink()
        shutil.rmtree(extract_dir)
        print(f"age installed to {install_dir}")
        print(f"Ensure {install_dir} is in your PATH")
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

    print("OK: age installed.")


def task_install_age() -> dict[str, Any]:
    """Install age encryption tool."""
    return {
        "actions": [_install_age],
        "title": title_with_actions,
        "verbosity": 2,
    }


def task_install_sops() -> dict[str, Any]:
    """Install SOPS secrets manager."""
    return create_install_task(
        name="sops",
        repo="getsops/sops",
        asset_patterns={
            "linux": "sops-v{version}.linux.amd64",
            "windows": "sops-v{version}.amd64.exe",
        },
        version_cmd=["sops", "--version"],
    )


def task_install_tools() -> dict[str, Any]:
    """Install all tools for SOPS credential encryption (age + sops)."""
    return {
        "actions": [lambda: print("All tools installed successfully!")],
        "task_dep": [
            "install_age",
            "install_sops",
        ],
        "title": title_with_actions,
        "verbosity": 2,
    }
