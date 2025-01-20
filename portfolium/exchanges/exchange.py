import abc

from portfolium.configs import *


class ExchangeHandler:

    @abc.abstractmethod
    def get_candle_stick_data(self, symbol: str, tf: str):
        pass

    def get_symbol(self, symbol: str) -> str:
        return symbol.replace("-", "")

    @staticmethod
    def is_symbol_eligible(historical_12h_data):
        """
        function to check if a given coin is eligible. Checks coins that have at least 46 days historical data
        :param historical_12h_data:
        :return: boolean
        """
        total_days_data = (len(historical_12h_data) * 4) / 24

        return total_days_data > COINS_HISTORY_DATA_THRESHOLD
