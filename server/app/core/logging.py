"""Structured logging configuration"""
import logging
import sys
from datetime import datetime
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """Configure application logging"""
    logger = logging.getLogger("cyber-risk")
    logger.setLevel(getattr(logging, settings.log_level.upper()))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)

        if settings.log_format.lower() == "json":
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
                '"module": "%(name)s", "message": "%(message)s"}'
            )
        else:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
            )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logging()
