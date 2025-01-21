from portfolium.configs import *
from portfolium.exchanges.exchange import ExchangeAPI
from portfolium.utils.logger import setup_logger

from binance.client import Client
import logging

# Initialize a logger
logger = setup_logger(LOGGER_NAME, LOG_LEVEL)

class Binance(ExchangeAPI):
    def __init__(self, api_key, api_secret, use_testnet=False):
        """
        Initialize the Binance client.

        Parameters:
        - api_key (str): Your Binance API key.
        - api_secret (str): Your Binance secret key.
        - use_testnet (bool): Use Binance Testnet if True.
        """
        try:
            self.client = Client(
                api_key=api_key,
                api_secret=api_secret,
                testnet=use_testnet
            )
            logger.info("Binance client initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing Binance client: {e}")
            self.client = None

    def get_positions(self):
        """
        Fetch active Binance Futures positions.

        Returns:
        - List of active positions (List[dict]).
        """
        if not self.client:
            logger.error("Client not initialized. Cannot fetch positions.")
            return []

        try:
            # Fetch all futures positions
            positions = self.client.futures_position_information()

            # Mapping of Binance keys to OKX-style names
            key_mapping = {
                "symbol": "instrument",
                "positionAmt": "position",
                "entryPrice": "average_price",
                "markPrice": "market_price",
                "liquidationPrice": "liquidation_price",
                "leverage": "leverage",
                "marginType": "margin_type",
                "isolatedMargin": "margin_ratio",
            }

            fields_to_keep = key_mapping.keys()  # Use the keys from the mapping

            # Simplify the JSON and rename keys
            simplified_positions = [
                {key_mapping[key]: item[key] for key in fields_to_keep if key in item}
                for item in positions if float(item["positionAmt"]) != 0  # Filter active positions
            ]

            logger.info(f"Successfully retrieved {len(simplified_positions)} positions.")
            return simplified_positions

        except Exception as e:
            logger.error(f"An error occurred while fetching positions: {e}")
            return []

    def get_balance(self):
        """
        Fetch the account balance from Binance.

        Returns:
        - List of balances (List[dict]).
        """
        if not self.client:
            logger.error("Client not initialized. Cannot fetch balance.")
            return []

        try:
            # Fetch account balance
            account_info = self.client.futures_account_balance()

            # Mapping of Binance keys to OKX-style names
            key_mapping = {
                "asset": "currency",
                "balance": "available_balance",
                "availableBalance": "usd_equivalent"
            }

            fields_to_keep = key_mapping.keys()  # Use the keys from the mapping

            # Simplify the JSON and rename keys
            simplified_balances = [
                {key_mapping[key]: item[key] for key in fields_to_keep if key in item}
                for item in account_info
            ]

            logger.info("Successfully retrieved balances.")
            return simplified_balances

        except Exception as e:
            logger.error(f"An error occurred while fetching balance: {e}")
            return []