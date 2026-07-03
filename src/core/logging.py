"""
Centralized logging configuration.

Provides structured logging across the entire application with a
consistent format for console and optional file output.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


LOGGER_NAME = "ai_data_investigator"


def configure_logging(
    level: int = logging.INFO,
    log_file: Path | None = None,
) -> logging.Logger:
    """
    Configure the application logger.

    Parameters
    ----------
    level
        Logging level.

    log_file
        Optional log file path.

    Returns
    -------
    logging.Logger
        Configured logger.
    """

    logger = logging.getLogger(LOGGER_NAME)

    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    console.setLevel(level)
    logger.addHandler(console)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)

        logger.addHandler(file_handler)

    return logger


def get_logger() -> logging.Logger:
    """Return the configured application logger."""
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        configure_logging()
    return logger