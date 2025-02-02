from portfolium.configs import *
from portfolium.exchanges.binance import Binance
from portfolium.exchanges.okx import OKX

class ExchangeManager:
    def __init__(self):
        self.exchanges = {}


    def create_exchanges(self, exchange_list):
        if not exchange_list:
            return
        
        if BINANCE_EXCHANGE in exchange_list:
            self.exchanges[BINANCE_EXCHANGE] = Binance(BINANCE_API_KEY, BINANCE_SECRET_KEY)

        if OKX_EXCHANGE in exchange_list:
            self.exchanges[OKX_EXCHANGE] = OKX(OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE)
            
