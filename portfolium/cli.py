from portfolium.configs import *
from portfolium.exchanges.binance import Binance
from portfolium.exchanges.okx import OKX
from portfolium.web.flask import app as flask_app
from portfolium.web.gunicorn import PortfoliumApp
from portfolium.utils.logger import setup_logger
from portfolium.exchanges.exchange_manager import ExchangeManager

import typer
import os
import time
import json
import logging

cli_app = typer.Typer()
logger = setup_logger(LOGGER_NAME, LOG_LEVEL)


@cli_app.command()
def test(file_name: str = typer.Argument("")):
    exchange_list = [BINANCE_EXCHANGE, OKX_EXCHANGE]

    exchange_manager = ExchangeManager()
    exchange_manager.create_exchanges(exchange_list)


@cli_app.command()
def server():
    """
    Start the server.
    """

    options = {
        "bind": "0.0.0.0:8000",
        "capture_output": True,
        "loglevel": LOG_LEVEL.lower()
    }

    PortfoliumApp(flask_app, options).run()
    logger.info("Started server...")

def main():
    cli_app()