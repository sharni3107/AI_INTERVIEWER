"""Simple shared logger so every module logs consistently."""

import logging
import sys

from app.core.config import settings


_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))

        logger.addHandler(handler)
        logger.setLevel(
            logging.DEBUG if settings.debug else logging.INFO
        )

        logger.propagate = False

    return logger