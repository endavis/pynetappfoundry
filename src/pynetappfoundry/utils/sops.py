"""SOPS encryption utilities for credential management.

This module provides a wrapper around the SOPS CLI tool for encrypting
and decrypting secrets using age encryption.
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess  # nosec B404
from pathlib import Path

logger = logging.getLogger(__name__)

# SOPS encrypted value prefix pattern
# Format: base64-encoded full SOPS JSON with metadata
SOPS_PREFIX = "SOPS["
SOPS_SUFFIX = "]"


class SOPSError(Exception):
    """Error from SOPS operations."""

    pass


class SOPSNotInstalledError(SOPSError):
    """SOPS CLI is not installed."""

    pass


class AgeNotInstalledError(SOPSError):
    """age CLI is not installed."""

    pass


def is_sops_installed() -> bool:
    """Check if SOPS CLI is installed.

    Returns:
        True if sops is available in PATH.
    """
    return shutil.which("sops") is not None


def is_age_installed() -> bool:
    """Check if age CLI is installed.

    Returns:
        True if age and age-keygen are available in PATH.
    """
    return shutil.which("age") is not None and shutil.which("age-keygen") is not None


def get_age_key_path() -> Path:
    """Get the default age key file path.

    Returns:
        Path to the age key file.
    """
    # Check SOPS_AGE_KEY_FILE env var first
    env_path = os.environ.get("SOPS_AGE_KEY_FILE")
    if env_path:
        return Path(env_path)

    # Default to ~/.sops/age/keys.txt
    return Path.home() / ".sops" / "age" / "keys.txt"


def generate_age_keypair(key_path: Path | None = None) -> tuple[str, str]:
    """Generate a new age keypair.

    Args:
        key_path: Path to save the private key. If None, uses default.

    Returns:
        Tuple of (public_key, private_key_path).

    Raises:
        AgeNotInstalledError: If age-keygen is not installed.
        SOPSError: If key generation fails.
    """
    if not is_age_installed():
        raise AgeNotInstalledError(
            "age is not installed. Install it with: brew install age (macOS) "
            "or see https://github.com/FiloSottile/age#installation"
        )

    if key_path is None:
        key_path = get_age_key_path()

    # Create directory if needed
    key_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate keypair
    try:
        result = subprocess.run(
            ["age-keygen", "-o", str(key_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        # age-keygen outputs public key to stderr
        output = result.stderr
    except subprocess.CalledProcessError as e:
        raise SOPSError(f"Failed to generate age keypair: {e.stderr}") from e

    # Extract public key from output
    # Format: "Public key: age1..."
    public_key = ""
    for line in output.splitlines():
        if line.startswith("Public key:"):
            public_key = line.split(":", 1)[1].strip()
            break

    if not public_key:
        # Try to read from the key file
        public_key = get_public_key_from_file(key_path)

    # Set restrictive permissions
    key_path.chmod(0o600)

    logger.info(f"Generated age keypair at {key_path}")
    return public_key, str(key_path)


def get_public_key_from_file(key_path: Path) -> str:
    """Extract public key from an age key file.

    Args:
        key_path: Path to the age key file.

    Returns:
        The public key string.

    Raises:
        SOPSError: If public key cannot be extracted.
    """
    if not key_path.exists():
        raise SOPSError(f"Age key file not found: {key_path}")

    content = key_path.read_text()
    for line in content.splitlines():
        if line.startswith("# public key:"):
            return line.split(":", 1)[1].strip()

    raise SOPSError(f"Could not find public key in {key_path}")


def is_encrypted(value: str) -> bool:
    """Check if a value is SOPS-encrypted.

    Args:
        value: The value to check.

    Returns:
        True if the value appears to be SOPS-encrypted.
    """
    return value.startswith(SOPS_PREFIX) and value.endswith(SOPS_SUFFIX)


def encrypt_value(value: str, public_key: str | None = None) -> str:
    """Encrypt a value using SOPS and age.

    Args:
        value: The plaintext value to encrypt.
        public_key: The age public key. If None, uses key from SOPS_AGE_KEY_FILE.

    Returns:
        The encrypted value with SOPS[...] wrapper containing base64-encoded
        full SOPS JSON (including metadata needed for decryption).

    Raises:
        SOPSNotInstalledError: If SOPS is not installed.
        SOPSError: If encryption fails.
    """
    import base64
    import json
    import tempfile

    if not is_sops_installed():
        raise SOPSNotInstalledError(
            "sops is not installed. Install it with: brew install sops (macOS) "
            "or see https://github.com/getsops/sops#installation"
        )

    # SOPS expects JSON input, we'll use a simple structure
    input_data = json.dumps({"value": value})

    # Use a temp file for cross-platform compatibility (no /dev/stdin on Windows)
    # Explicitly use UTF-8 encoding for Windows compatibility with unicode
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as tmp_file:
        tmp_file.write(input_data)
        tmp_path = tmp_file.name

    try:
        # Build command
        cmd = ["sops", "--encrypt", "--input-type", "json", "--output-type", "json"]

        if public_key:
            cmd.extend(["--age", public_key])

        cmd.append(tmp_path)

        # Use UTF-8 encoding for subprocess output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as e:
        raise SOPSError(f"SOPS encryption failed: {e.stderr}") from e
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    # Validate JSON output
    try:
        json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise SOPSError(f"Failed to parse SOPS output: {e}") from e

    # Store the full SOPS JSON (base64 encoded) to preserve metadata for decryption
    encoded = base64.b64encode(result.stdout.encode()).decode()
    return f"{SOPS_PREFIX}{encoded}{SOPS_SUFFIX}"


def decrypt_value(encrypted_value: str) -> str:
    """Decrypt a SOPS-encrypted value.

    Args:
        encrypted_value: The encrypted value in SOPS[base64...] format,
            or legacy ENC[...] format (which will fail without metadata).

    Returns:
        The decrypted plaintext value.

    Raises:
        SOPSNotInstalledError: If SOPS is not installed.
        SOPSError: If decryption fails.
    """
    import base64
    import json

    if not is_sops_installed():
        raise SOPSNotInstalledError(
            "sops is not installed. Install it with: brew install sops (macOS) "
            "or see https://github.com/getsops/sops#installation"
        )

    # Extract base64 content and decode to get full SOPS JSON
    if not (encrypted_value.startswith(SOPS_PREFIX) and encrypted_value.endswith(SOPS_SUFFIX)):
        raise SOPSError(
            f"Unknown encrypted value format. Expected SOPS[...], got: {encrypted_value[:20]}..."
        )

    b64_content = encrypted_value[len(SOPS_PREFIX) : -len(SOPS_SUFFIX)]
    try:
        input_data = base64.b64decode(b64_content).decode()
    except Exception as e:
        raise SOPSError(f"Failed to decode SOPS value: {e}") from e

    # Use a temp file for cross-platform compatibility (no /dev/stdin on Windows)
    # Explicitly use UTF-8 encoding for Windows compatibility with unicode
    import tempfile

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as tmp_file:
        tmp_file.write(input_data)
        tmp_path = tmp_file.name

    try:
        # Build command
        cmd = ["sops", "--decrypt", "--input-type", "json", "--output-type", "json"]
        cmd.append(tmp_path)

        # Use UTF-8 encoding for subprocess output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as e:
        raise SOPSError(f"SOPS decryption failed: {e.stderr}") from e
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    # Parse the decrypted JSON and extract the value
    try:
        decrypted_data = json.loads(result.stdout)
        return str(decrypted_data.get("value", ""))
    except json.JSONDecodeError as e:
        raise SOPSError(f"Failed to parse SOPS output: {e}") from e


def create_sops_config(
    config_path: Path,
    public_keys: list[str],
    path_regex: str = r".*\.toml$",
) -> None:
    """Create a .sops.yaml configuration file.

    Args:
        config_path: Path to write the .sops.yaml file.
        public_keys: List of age public keys.
        path_regex: Regex pattern for files to encrypt.
    """
    import yaml

    config = {
        "creation_rules": [
            {
                "path_regex": path_regex,
                "age": ",".join(public_keys),
            }
        ]
    }

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    logger.info(f"Created SOPS config at {config_path}")
