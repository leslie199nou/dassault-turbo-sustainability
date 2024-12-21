from config import ConfigKeys
import sys
import os
import logging

logger = logging.getLogger(__name__)


def check_path(app, key_value: str):
    if not os.path.exists(app.config.get(key_value)):
        logger.error(f"The path: {key_value} is not accessible")
        sys.exit()


def check_startup(app):
    check_path(app, ConfigKeys.APP_DOWNLOAD_DIRECTORY.value)
    check_path(app, ConfigKeys.APP_CSV_PATH.value)

    for key in ConfigKeys:
        if app.config.get(key.value) is None:
            logger.error(f"Please complete all the fields in the configuration file")
            logger.error(f"The field {key.value} is not set in the configuration file")
            sys.exit()

    for key, conf in app.config.items():
        if key.startswith('APP_') or key.startswith('TURBONOMIC_'):
            if not conf:
                logger.error(f"Please complete all the fields in the configuration file")
                logger.error(f"The field {key} is not valid with the value: '{conf}'")
                sys.exit()
