"""Logging utilities for tactile art transform."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    console: bool = True,
) -> logging.Logger:
    """Set up logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        console: Whether to log to console

    Returns:
        Configured logger instance

    Raises:
        ValueError: If level is invalid
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")

    # Create logger
    logger = logging.getLogger("art_tactile_transform")
    logger.setLevel(numeric_level)

    # Clear existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Optional logger name (defaults to main package logger)

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"art_tactile_transform.{name}")
    return logging.getLogger("art_tactile_transform")


class ProgressLogger:
    """Simple progress logger for long-running operations."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize progress logger.

        Args:
            logger: Optional logger instance (defaults to package logger)
        """
        self.logger = logger or get_logger()
        self.current_step = 0
        self.total_steps = 0

    def start(self, total_steps: int, description: str = "Processing") -> None:
        """Start a progress tracking session.

        Args:
            total_steps: Total number of steps
            description: Description of the operation
        """
        self.current_step = 0
        self.total_steps = total_steps
        self.logger.info(f"{description}: 0/{total_steps} steps")

    def step(self, description: Optional[str] = None) -> None:
        """Log completion of a step.

        Args:
            description: Optional description of the completed step
        """
        self.current_step += 1
        msg = f"Step {self.current_step}/{self.total_steps}"
        if description:
            msg += f": {description}"
        self.logger.info(msg)

    def complete(self, description: str = "Complete") -> None:
        """Log completion of all steps.

        Args:
            description: Completion message
        """
        self.logger.info(f"{description}: {self.current_step}/{self.total_steps} steps")
