from portfolium.configs import *
from portfolium.exchanges.binance import Binance
from portfolium.exchanges.okx import OKX
from portfolium.web.flask import app as flask_app
from portfolium.web.gunicorn import PortfoliumApp
from portfolium.utils.logger import setup_logger

import typer
import os
import time
import json
import logging

cli_app = typer.Typer()
logger = setup_logger(LOGGER_NAME, LOG_LEVEL)


@cli_app.command()
def test(file_name: str = typer.Argument("")):

    okx = OKX(OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE)
    binance = Binance(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    EXCHANGES[OKX_EXCHANGE] = okx
    EXCHANGES[BINANCE_EXCHANGE] = binance

    balance = EXCHANGES[OKX_EXCHANGE].get_positions()
    logger.info(json.dumps(balance, indent=4))


@cli_app.command()
def server():
    """
    Start the server.
    """

    okx = OKX(OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE)
    binance = Binance(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    EXCHANGES[OKX_EXCHANGE] = okx
    EXCHANGES[BINANCE_EXCHANGE] = binance

    options = {
        "bind": "0.0.0.0:8000",
        "capture_output": True,
        "loglevel": LOG_LEVEL.lower()
    }

    PortfoliumApp(flask_app, options).run()
    logger.info("Started server...")

def main():
    cli_app()