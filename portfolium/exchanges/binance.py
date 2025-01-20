from portfolium.configs import *

from binance.client import Client


def fetch_futures_positions(api_key, api_secret, testnet=False):
    """
    Fetch and display active Binance Futures positions.

    Parameters:
    - api_key (str): Your Binance API key.
    - api_secret (str): Your Binance secret key.
    - testnet (bool): Set to True to use Binance Futures Testnet.

    Returns:
    - List of active positions with details.
    """
    try:
        # Initialize the Binance client
        client = Client(api_key, api_secret, testnet=testnet)

        # Fetch all futures positions
        positions = client.futures_position_information()

        return positions

    except Exception as e:
        print(f"An error occurred: {e}")
        return []