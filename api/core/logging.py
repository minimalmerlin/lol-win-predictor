"""
Logging configuration for the application
"""

import logging
import sys


def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Get logger for the app
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    return logger


# Global logger instance
logger = setup_logging()
