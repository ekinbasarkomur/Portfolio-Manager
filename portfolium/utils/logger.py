from portfolium.configs import *

import logging
import os
import datetime

def setup_logger(logger_name="AppLogger", log_level=logging.INFO):
    """
    Set up a centralized logger for the application.

    Parameters:
        logger_name (str): The name of the logger.
        log_level (int): The logging level (e.g., logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Define log directory and file
    # Configure logger
    logger = logging.getLogger(logger_name)
    if not logger.handlers:  # Avoid duplicate handlers
        logger.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        # File handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)  # Explicitly set level
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)  # Explicitly set level
        logger.addHandler(console_handler)

    return logger