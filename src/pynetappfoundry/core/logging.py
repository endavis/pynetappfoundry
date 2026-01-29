"""Logging configuration module."""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(script_name: str) -> logging.Logger:
    """Set up logging for a script with file handler only.

    Console output is handled by Rich via cli/utils.py print functions.
    This logger only writes to file for debugging and audit purposes.

    Args:
        script_name: Name of the script (used for log directory and file naming).

    Returns:
        The configured root logger.
    """
    root_logger = logging.getLogger()
    # Don't set root logger to DEBUG - some libraries (netapp_ontap) crash
    # The file handler will capture DEBUG messages for pynetappfoundry
    root_logger.setLevel(logging.DEBUG)

    log_dir = Path(os.getcwd()) / "data" / script_name / "logs"
    os.makedirs(log_dir, exist_ok=True)

    # create a formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # add a file handler only - console output is handled by Rich
    log_filename = datetime.now().strftime(
        f"data/{script_name}/logs/{script_name}_%Y-%m-%d_%H-%M-%S.log"
    )
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    return root_logger
