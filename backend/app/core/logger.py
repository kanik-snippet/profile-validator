import logging

from app.core.config import get_settings


def configure_logger() -> logging.Logger:
    settings = get_settings()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        force=True,
    )

    logger = logging.getLogger(settings.app_name)

    logger.info("Logger initialized.")

    return logger


logger = configure_logger()