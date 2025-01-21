from portfolium.configs import *
from portfolium.exchanges.exchange import ExchangeAPI
from portfolium.utils.logger import setup_logger

import okx.Account as Account

logger = setup_logger(LOGGER_NAME, LOG_LEVEL)

class OKX(ExchangeAPI):
    def __init__(self, api_key, api_secret, passphrase, use_testnet=False):
        """
        Initialize the OKX client.

        Parameters:
        - api_key (str): Your OKX API key.
        - api_secret (str): Your OKX API secret key.
        - passphrase (str): Your OKX passphrase.
        - use_testnet (bool): Use OKX Testnet if True.
        """
        try:
            self.client = Account.AccountAPI(
                api_key,
                api_secret,
                passphrase,
                use_server_time=True,
                flag='1' if use_testnet else '0'  # '1' for testnet, '0' for production
            )
            logger.info("OKX client initialized successfully.")
        except Exception as e:
            logger.info(f"Error initializing OKX Account API client: {e}")
            self.client = None


    def get_positions(self):
        """
        Fetch active OKX futures positions.

        Returns:
        - List of active positions (List[dict]).
        """
        if not self.client:
            logger.info("Client not initialized. Cannot fetch positions.")
            return []

        try:
            # Fetch all positions
            response = self.client.get_positions()

            # Check response status
            if response.get('code') == '0':  # Success code
                positions = response.get('data', [])

                # Mapping of original keys to meaningful names
                key_mapping = {
                    "instId": "instrument",
                    "pos": "position",
                    "posSide": "side",
                    "lever": "leverage",
                    "avgPx": "average_price",
                    "markPx": "market_price",
                    "liqPx": "liquidation_price",
                    "mgnRatio": "margin_ratio",
                    "closeOrderAlgo": "close_orders"
                }

                fields_to_keep = key_mapping.keys()  # Use the keys from the mapping

                # Simplify the JSON and rename keys
                positions = [
                    {key_mapping[key]: item[key] for key in fields_to_keep if key in item}
                    for item in positions
                ]

                # Log the count of active positions retrieved
                logger.info(f"Successfully retrieved {len(positions)} positions.")
                return positions
            else:
                # Log the error message from the response
                error_message = response.get('msg', 'Unknown error')
                logger.error(f"Error fetching positions: {error_message}")
                return []

        except Exception as e:
            # Log any exception that occurs
            logger.error(f"An error occurred while fetching positions: {e}")
            return []
        


    def get_balance(self):
        """
        Fetch the account balance from OKX.

        Returns:
        - List of balances (List[dict]).
        """
        if not self.client:
            logger.info("Client not initialized. Cannot fetch balance.")
            return []

        try:
            # Fetch the account balance
            response = self.client.get_account_balance()

            # Check response status
            if response.get('code') == '0':  # Success code
                balances = response.get('data', [])

                # Mapping of original keys to meaningful names
                key_mapping = {
                    "ccy": "currency",
                    "availBal": "available_balance",
                    "eqUsd": "usd_equivalent"
                }

                fields_to_keep = key_mapping.keys()  # Use the keys from the mapping

                # Simplify the JSON and rename keys
                balances = balances[0]['details']

                balances = [
                    {key_mapping[key]: item[key] for key in fields_to_keep if key in item}
                    for item in balances
                ]


                logger.info("Successfully retrieved balances.")
                return balances
            else:
                error_message = response.get('msg', 'Unknown error')
                logger.error(f"Error fetching balance: {error_message}")
                return []

        except Exception as e:
            logger.error(f"An error occurred while fetching balance: {e}")
            return []