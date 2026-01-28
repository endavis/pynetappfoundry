"""Logging configuration module."""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(script_name: str) -> logging.Logger:
    """Set up logging for a script with both console and file handlers.

    Args:
        script_name: Name of the script (used for log directory and file naming).

    Returns:
        The configured root logger.
    """
    root_logger = logging.getLogger()
    # Don't set root logger to DEBUG - some libraries (netapp_ontap) crash
    # The file handler will capture DEBUG messages for pynetappfoundry
    root_logger.setLevel(logging.INFO)

    log_dir = Path(os.getcwd()) / "data" / script_name / "logs"
    os.makedirs(log_dir, exist_ok=True)

    # create a formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # add a console handler, default INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # add a file handler, default DEBUG
    log_filename = datetime.now().strftime(
        f"data/{script_name}/logs/{script_name}_%Y-%m-%d_%H-%M-%S.log"
    )
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    return root_logger
