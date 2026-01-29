"""Initialize SOPS encryption for credentials."""

from __future__ import annotations

import shutil
from pathlib import Path

import click
from rich.console import Console

from pynetappfoundry.cli.utils import print_error, print_success, print_warning
from pynetappfoundry.utils.sops import (
    AgeNotInstalledError,
    SOPSError,
    generate_age_keypair,
    get_age_key_path,
    get_public_key_from_file,
    is_age_installed,
    is_sops_installed,
)

console = Console()


def _update_envrc_local(key_path: str) -> bool:
    """Update .envrc.local with SOPS_AGE_KEY_FILE export.

    Args:
        key_path: Path to the age key file.

    Returns:
        True if .envrc.local was updated, False otherwise.
    """
    envrc_local = Path.cwd() / ".envrc.local"
    envrc_example = Path.cwd() / ".envrc.local.example"
    export_line = f'export SOPS_AGE_KEY_FILE="{key_path}"'

    # Copy from example if .envrc.local doesn't exist
    if not envrc_local.exists():
        if envrc_example.exists():
            shutil.copy(envrc_example, envrc_local)
            console.print(f"Created {envrc_local} from {envrc_example}")
        else:
            # Create minimal .envrc.local
            envrc_local.write_text("# Personal direnv overrides\n# This file is git-ignored\n\n")
            console.print(f"Created {envrc_local}")

    # Read current content
    content = envrc_local.read_text()

    # Check if SOPS_AGE_KEY_FILE is already set
    if "SOPS_AGE_KEY_FILE" in content:
        # Update existing line
        lines = content.splitlines()
        new_lines = []
        for line in lines:
            if "SOPS_AGE_KEY_FILE" in line and not line.strip().startswith("#"):
                new_lines.append(export_line)
            else:
                new_lines.append(line)
        envrc_local.write_text("\n".join(new_lines) + "\n")
        console.print(f"Updated SOPS_AGE_KEY_FILE in {envrc_local}")
    else:
        # Append new line
        with open(envrc_local, "a") as f:
            f.write("\n# SOPS age key for credential encryption\n")
            f.write(f"{export_line}\n")
        console.print(f"Added SOPS_AGE_KEY_FILE to {envrc_local}")

    return True


def _save_public_key(public_key: str) -> None:
    """Save public key to a file and ensure it's in .gitignore.

    Args:
        public_key: The age public key string.
    """
    public_key_file = Path.cwd() / ".sops-public-key.txt"
    gitignore_file = Path.cwd() / ".gitignore"
    gitignore_entry = ".sops-public-key.txt"

    # Write public key to file
    public_key_file.write_text(f"# Age public key for SOPS encryption\n{public_key}\n")
    console.print(f"Saved public key to {public_key_file}")

    # Ensure it's in .gitignore
    if gitignore_file.exists():
        content = gitignore_file.read_text()
        if gitignore_entry not in content:
            with open(gitignore_file, "a") as f:
                f.write(f"\n# SOPS public key file\n{gitignore_entry}\n")
            console.print(f"Added {gitignore_entry} to .gitignore")
    else:
        gitignore_file.write_text(f"# SOPS public key file\n{gitignore_entry}\n")
        console.print(f"Created .gitignore with {gitignore_entry}")


@click.command("init-sops")
@click.option(
    "--key-path",
    type=click.Path(path_type=Path),
    help="Path to store the age private key. Default: ~/.sops/age/keys.txt",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing key file.",
)
@click.pass_context
def init_sops(ctx: click.Context, key_path: Path | None, force: bool) -> None:
    """Initialize SOPS encryption with age for credential storage.

    This command:

    1. Checks that sops and age are installed

    2. Generates an age keypair for encrypting credentials

    3. Displays the public key for sharing with team members

    Example:

        nf config init-sops

        nf config init-sops --key-path ~/.my-keys/age.txt
    """
    # Check prerequisites
    if not is_sops_installed():
        print_error("SOPS is not installed.")
        console.print("\nInstall SOPS:")
        console.print("  macOS: brew install sops")
        console.print("  Linux: See https://github.com/getsops/sops#installation")
        ctx.exit(1)

    if not is_age_installed():
        print_error("age is not installed.")
        console.print("\nInstall age:")
        console.print("  macOS: brew install age")
        console.print("  Linux: See https://github.com/FiloSottile/age#installation")
        ctx.exit(1)

    # Determine key path
    if key_path is None:
        key_path = get_age_key_path()

    # Check if key already exists
    if key_path.exists() and not force:
        print_warning(f"Age key already exists at {key_path}")
        try:
            public_key = get_public_key_from_file(key_path)
            console.print(f"\nYour public key: [bold]{public_key}[/bold]")
            console.print("\nUse --force to generate a new keypair.")
        except SOPSError as e:
            print_error(f"Could not read existing key: {e}")
        ctx.exit(0)

    # Delete existing key file if force is used
    if force and key_path.exists():
        key_path.unlink()
        console.print(f"Removed existing key at {key_path}")

    # Generate keypair
    try:
        console.print(f"Generating age keypair at {key_path}...")
        public_key, private_key_path = generate_age_keypair(key_path)
    except AgeNotInstalledError as e:
        print_error(str(e))
        ctx.exit(1)
    except SOPSError as e:
        print_error(f"Failed to generate keypair: {e}")
        ctx.exit(1)

    print_success("Age keypair generated successfully!")
    console.print()
    console.print(f"Private key: [dim]{private_key_path}[/dim]")
    console.print(f"Public key:  [bold]{public_key}[/bold]")
    console.print()

    # Update .envrc.local with SOPS_AGE_KEY_FILE
    _update_envrc_local(private_key_path)

    # Save public key to file
    _save_public_key(public_key)
    console.print()

    console.print("[yellow]Important:[/yellow]")
    console.print("  1. Keep your private key secure - never share it")
    console.print("  2. Share your public key with team members who need access")
    console.print("  3. Run 'direnv allow' to load the environment variable")
    console.print()
    console.print("Next steps:")
    console.print("  direnv allow                                # Load env vars")
    console.print("  nf config set-credential --cluster <name>   # Encrypt a password")
