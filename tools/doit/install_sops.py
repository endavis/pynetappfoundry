"""Project-specific install tasks for SOPS credential encryption.

- age: Encryption tool for SOPS
- sops: Secrets management

Kept separate from ``install_tools.py`` (the reusable framework synced
from the upstream pyproject-template) so template refreshes do not
overwrite these project-specific tasks.

The ``_install_age`` helper is custom because the upstream framework's
``extract_binaries`` parameter is a single list applied across all
platforms, which cannot express ``age`` vs ``age.exe`` per OS. Once
https://github.com/endavis/pyproject-template/issues/477 lands this
helper can collapse into a single ``create_install_task`` call.
"""

import glob
import os
import platform
import shutil
import subprocess  # nosec B404 - subprocess is required for version checks
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

from doit.tools import title_with_actions

from tools.doit.install_tools import (
    create_install_task,
    get_install_dir,
    get_latest_github_release,
)


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
        tar_url = (
            f"https://github.com/FiloSottile/age/releases/download/v{version}/"
            f"age-v{version}-linux-amd64.tar.gz"
        )
        tar_path = Path("/tmp/age.tar.gz")  # nosec B108
        print(f"Downloading {tar_url}...")
        urllib.request.urlretrieve(tar_url, tar_path)  # nosec B310

        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall("/tmp")  # nosec B202 B108

        for binary in ["age", "age-keygen"]:
            src = Path("/tmp/age") / binary  # nosec B108
            dst = install_dir / binary
            shutil.move(str(src), str(dst))
            dst.chmod(0o755)  # nosec B103

        tar_path.unlink()
        shutil.rmtree("/tmp/age", ignore_errors=True)  # nosec B108
    elif system == "darwin":
        subprocess.run(["brew", "install", "age"], check=True)
    elif system == "windows":
        zip_url = (
            f"https://github.com/FiloSottile/age/releases/download/v{version}/"
            f"age-v{version}-windows-amd64.zip"
        )
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
