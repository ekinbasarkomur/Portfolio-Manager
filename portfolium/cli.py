from portfolium.configs import *
from portfolium.exchanges.binance import fetch_futures_positions

import typer
import os
import time


app = typer.Typer()


@app.command()
def positions(file_name: str = typer.Argument("")):
    positions = fetch_futures_positions(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    print(positions)


def main():
    app()