from portfolium.configs import *
from portfolium.exchanges.exchange import ExchangeAPI
from portfolium.utils.logger import setup_logger

import okx.Account as Account
import pandas as pd

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
        Fetch active OKX futures positions and return them as a Pandas DataFrame.

        Returns:
        - Pandas DataFrame with selected columns.
        """
        if not self.client:
            logger.info("Client not initialized. Cannot fetch positions.")
            return pd.DataFrame()  # Return an empty DataFrame

        try:
            # Fetch all positions from OKX API
            response = self.client.get_positions()

            # Check response status
            if response.get('code') == '0':  # Success code
                fetched_positions = response.get('data', [])

                if not fetched_positions:
                    logger.info("No active positions found.")
                    return pd.DataFrame()

                # Define only the keys we want to keep
                selected_keys = [
                    "instId", "pos", "posSide", "avgPx", "markPx", "lever",
                    "liqPx", "upl", "margin"
                ]

                # Extract only selected keys
                formatted_positions = [{key: item[key] for key in selected_keys if key in item} for item in fetched_positions]

                # Convert list of dicts to DataFrame
                positions_df = pd.DataFrame(formatted_positions)

                # Rename columns to meaningful names
                positions_df.rename(columns={
                    "instId": "symbol",
                    "pos": "position_size",
                    "posSide": "position_type",
                    "avgPx": "avg_price",
                    "markPx": "market_price",
                    "lever": "leverage",
                    "liqPx": "liquidation_price",
                    "upl": "profit",
                    "margin": "margin_used"
                }, inplace=True)

                # Add exchange column
                positions_df["exchange"] = OKX_EXCHANGE

                # Extract Take Profit (tpTriggerPx) & Stop Loss (slTriggerPx) from close_orders
                positions_df["take_profit"] = [
                    next((order.get("tpTriggerPx") for order in item.get("close_orders", []) if "tpTriggerPx" in order), None)
                    for item in fetched_positions
                ]
                positions_df["stop_loss"] = [
                    next((order.get("slTriggerPx") for order in item.get("close_orders", []) if "slTriggerPx" in order), None)
                    for item in fetched_positions
                ]

                # Log the count of active positions retrieved
                logger.info(f"Successfully retrieved {len(positions_df)} positions.")
                return positions_df

            else:
                # Log API error message
                error_message = response.get('msg', 'Unknown error')
                logger.error(f"Error fetching positions: {error_message}")
                return pd.DataFrame()

        except Exception as e:
            # Log unexpected errors
            logger.error(f"An error occurred while fetching positions: {e}")
            return pd.DataFrame()
        


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