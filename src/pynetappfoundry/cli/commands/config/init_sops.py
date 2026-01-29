"""Initialize SOPS encryption for credentials."""

from __future__ import annotations

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
    console.print("[yellow]Important:[/yellow]")
    console.print("  1. Keep your private key secure - never share it")
    console.print("  2. Share your public key with team members who need access")
    console.print("  3. Set SOPS_AGE_KEY_FILE environment variable:")
    console.print(f"     export SOPS_AGE_KEY_FILE={private_key_path}")
    console.print()
    console.print("Next steps:")
    console.print("  nf config set-credential --cluster <name>  # Encrypt a password")
