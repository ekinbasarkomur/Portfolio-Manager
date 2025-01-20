import typer
import os

from portfolio_manager.configs import *
import time

app = typer.Typer()


@app.command()
def test(file_name: str = typer.Argument("")):
    print('test')



def main():
    app()