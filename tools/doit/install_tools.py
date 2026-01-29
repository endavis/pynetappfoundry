"""Tool installation tasks for SOPS credential encryption.

Installs external tools required for encrypted credential management:
- age: Encryption tool for SOPS
- sops: Secrets management
"""

import json
import os
import platform
import shutil
import subprocess  # nosec B404
import sys
import urllib.request
from typing import Any

from doit.tools import title_with_actions


def _run_cmd(cmd: str, shell: bool = True, check: bool = True) -> None:
    """Run a shell command."""
    print(f"Executing: {cmd}")
    subprocess.run(cmd, shell=shell, check=check)  # nosec B602


def _get_latest_github_release(repo: str) -> str:
    """Get latest release version from GitHub."""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    request = urllib.request.Request(url)

    # Use GitHub token if available to avoid rate limits
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        request.add_header("Authorization", f"token {github_token}")

    with urllib.request.urlopen(request) as response:  # nosec B310
        data = json.loads(response.read().decode())
        return str(data["tag_name"]).lstrip("v")


def _get_install_dir() -> str:
    """Get the installation directory for tools."""
    system = platform.system().lower()
    if system == "windows":
        # Use a tools directory in user profile on Windows
        install_dir = os.path.join(os.environ.get("USERPROFILE", ""), ".local", "bin")
    else:
        install_dir = os.path.expanduser("~/.local/bin")
    os.makedirs(install_dir, exist_ok=True)
    return install_dir


def _install_age() -> None:
    """Install age encryption tool."""
    if shutil.which("age"):
        print(f"age already installed: {subprocess.getoutput('age --version')}")  # nosec B607 B603
        return

    print("Installing age...")
    version = _get_latest_github_release("FiloSottile/age")
    print(f"Latest version: {version}")

    system = platform.system().lower()
    install_dir = _get_install_dir()

    if system == "linux":
        tar_url = f"https://github.com/FiloSottile/age/releases/download/v{version}/age-v{version}-linux-amd64.tar.gz"
        tar_path = "/tmp/age.tar.gz"  # nosec B108
        print(f"Downloading {tar_url}...")
        urllib.request.urlretrieve(tar_url, tar_path)  # nosec B310

        import tarfile

        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall("/tmp")  # nosec B202
        _run_cmd(f"mv /tmp/age/age /tmp/age/age-keygen {install_dir}/")
        _run_cmd(f"chmod +x {install_dir}/age {install_dir}/age-keygen")
        os.remove(tar_path)
        _run_cmd("rm -rf /tmp/age")
    elif system == "darwin":
        _run_cmd("brew install age")
    elif system == "windows":
        import zipfile

        zip_url = f"https://github.com/FiloSottile/age/releases/download/v{version}/age-v{version}-windows-amd64.zip"
        zip_path = os.path.join(os.environ.get("TEMP", "."), "age.zip")
        extract_dir = os.path.join(os.environ.get("TEMP", "."), "age_extract")
        print(f"Downloading {zip_url}...")
        urllib.request.urlretrieve(zip_url, zip_path)  # nosec B310

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)  # nosec B202

        # Find and move executables
        for exe in ["age.exe", "age-keygen.exe"]:
            src = os.path.join(extract_dir, f"age-v{version}-windows-amd64", exe)
            dst = os.path.join(install_dir, exe)
            shutil.move(src, dst)

        os.remove(zip_path)
        shutil.rmtree(extract_dir)
        print(f"age installed to {install_dir}")
        print(f"Ensure {install_dir} is in your PATH")
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)
    print("age installed")


def _install_sops() -> None:
    """Install SOPS secrets manager."""
    if shutil.which("sops"):
        version_output = subprocess.getoutput("sops --version").splitlines()[0]  # nosec B607 B603
        print(f"SOPS already installed: {version_output}")
        return

    print("Installing SOPS...")
    version = _get_latest_github_release("getsops/sops")
    print(f"Latest version: {version}")

    system = platform.system().lower()
    install_dir = _get_install_dir()

    if system == "linux":
        bin_url = f"https://github.com/getsops/sops/releases/download/v{version}/sops-v{version}.linux.amd64"
        bin_path = os.path.join(install_dir, "sops")
        print(f"Downloading {bin_url}...")
        urllib.request.urlretrieve(bin_url, bin_path)  # nosec B310
        _run_cmd(f"chmod +x {bin_path}")
    elif system == "darwin":
        _run_cmd("brew install sops")
    elif system == "windows":
        bin_url = (
            f"https://github.com/getsops/sops/releases/download/v{version}/sops-v{version}.exe"
        )
        bin_path = os.path.join(install_dir, "sops.exe")
        print(f"Downloading {bin_url}...")
        urllib.request.urlretrieve(bin_url, bin_path)  # nosec B310
        print(f"SOPS installed to {install_dir}")
        print(f"Ensure {install_dir} is in your PATH")
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)
    print(f"SOPS {version} installed")


def task_install_age() -> dict[str, Any]:
    """Install age encryption tool."""
    return {
        "actions": [_install_age],
        "title": title_with_actions,
        "verbosity": 2,
    }


def task_install_sops() -> dict[str, Any]:
    """Install SOPS secrets manager."""
    return {
        "actions": [_install_sops],
        "title": title_with_actions,
        "verbosity": 2,
    }


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
