"""Logging configuration for Kiro Automation Framework."""

import logging
import json
from datetime import datetime
from pathlib import Path


class FrameworkLogger:
    """Centralized logging for framework operations."""

    def __init__(self, name="kiro_automation", log_file=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            )

            console = logging.StreamHandler()
            console.setFormatter(formatter)
            self.logger.addHandler(console)

            if log_file:
                Path(log_file).parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def info(self, event, **kwargs):
        msg = f"{event}"
        if kwargs:
            msg += f" | {json.dumps(kwargs)}"
        self.logger.info(msg)

    def warning(self, event, **kwargs):
        msg = f"{event}"
        if kwargs:
            msg += f" | {json.dumps(kwargs)}"
        self.logger.warning(msg)

    def error(self, event, **kwargs):
        msg = f"{event}"
        if kwargs:
            msg += f" | {json.dumps(kwargs)}"
        self.logger.error(msg)


# Global logger instance
_logger = None


def get_logger(log_file=None):
    """Get or create global logger instance."""
    global _logger
    if _logger is None:
        _logger = FrameworkLogger(log_file=log_file)
    return _logger
