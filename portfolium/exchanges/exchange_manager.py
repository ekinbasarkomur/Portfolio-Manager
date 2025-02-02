from portfolium.configs import *
from portfolium.exchanges.binance import Binance
from portfolium.exchanges.okx import OKX

import pandas as pd

class ExchangeManager:
    def __init__(self):
        self.exchanges = {}
        self.positions = pd.DataFrame(columns=[
            "exchange", "symbol", "position_size",
            "position_type", "avg_price", "market_price", 
            "profit", "leverage", "margin_used", 
            "market_price", "take_profit","stop_loss", 
            "liquidation_price", "money_at_risk"
        ])


    def create_exchanges(self, exchange_list):
        if not exchange_list:
            return
        
        if BINANCE_EXCHANGE in exchange_list:
            self.exchanges[BINANCE_EXCHANGE] = Binance(BINANCE_API_KEY, BINANCE_SECRET_KEY)

        if OKX_EXCHANGE in exchange_list:
            self.exchanges[OKX_EXCHANGE] = OKX(OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE)
            


    def get_positions(self):
        positions = self.positions.copy()  # Make a copy of the existing positions DataFrame

        for exchange_name, exchange in self.exchanges.items():
            exchange_positions = exchange.get_positions()
            return exchange_positions
            #return pd.concat([positions, exchange_positions], ignore_index=True)

        return positions