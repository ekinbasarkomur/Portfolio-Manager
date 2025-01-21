from portfolium.utils.logger import setup_logger
from gunicorn.app.base import BaseApplication
import logging

class PortfoliumApp(BaseApplication):
    def __init__(self, app, options=None):
        """
        Custom Gunicorn application wrapper for integrating Flask with custom options and centralized logging.

        Parameters:
        - app: The Flask application instance.
        - options: A dictionary of Gunicorn configuration options.
        """
        self.app = app
        self.options = options or {}
        self.logger = setup_logger()  # Centralized logger
        if not isinstance(self.logger, logging.Logger):
            raise RuntimeError("Logger setup failed. `setup_logger` did not return a valid logger.")
        
        self.logger.info("PortfoliumApp initialized.")
        
        super().__init__()

    def load_config(self):
        """
        Load and apply the Gunicorn configuration from the provided options.
        """
        # Reinitialize the logger to ensure consistency
        if not self.logger or not self.logger.handlers:
            self.logger = setup_logger()
            self.logger.warning("Logger reinitialized in load_config due to missing handlers.")

        # Apply Gunicorn options
        for key, value in self.options.items():
            if key.lower() in self.cfg.settings:
                self.cfg.set(key.lower(), value)

        # Redirect Gunicorn's error logger to the centralized logger
        gunicorn_error_logger = logging.getLogger("gunicorn.error")
        gunicorn_access_logger = logging.getLogger("gunicorn.access")

        # Remove Gunicorn's default StreamHandler
        if gunicorn_error_logger:
            self.logger.info("Removing Gunicorn's default StreamHandler.")
            gunicorn_error_logger.handlers = []  # Remove handlers to prevent duplicate logging

        # Remove Gunicorn's default StreamHandler
        if gunicorn_access_logger:
            self.logger.info("Removing Gunicorn's default StreamHandler.")
            gunicorn_access_logger.handlers = []  # Remove handlers to prevent duplicate logging


        # Add centralized logger's handlers to Gunicorn
        for handler in self.logger.handlers:
            gunicorn_error_logger.addHandler(handler)
            gunicorn_access_logger.addHandler(handler)

        # Synchronize log levels
        gunicorn_error_logger.setLevel(self.logger.level)
        gunicorn_access_logger.setLevel(self.logger.level)

        self.logger.info("Gunicorn loggers have been integrated with the centralized logger.")
        self.logger.debug(f"Gunicorn error logger handlers: {gunicorn_error_logger.handlers}")

    def load(self):
        """
        Return the Flask application instance.
        """
        return self.app