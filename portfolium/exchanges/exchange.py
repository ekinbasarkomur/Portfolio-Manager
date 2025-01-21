import abc

from portfolium.configs import *
    
class ExchangeAPI:
    def __init__(self, api_key, api_secret, use_testnet=False):
        """
        Initialize the Exchange client.

        Parameters:
        - api_key (str): Your API key.
        - api_secret (str): Your API secret key.
        - use_testnet (bool): Use the Testnet if True.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.use_testnet = use_testnet
        self.client = None

    @abc.abstractmethod
    def initialize_client(self):
        """Abstract method to initialize the exchange client."""
        pass

    @abc.abstractmethod
    def get_positions(self):
        """Abstract method to fetch futures positions."""
        pass

    @abc.abstractmethod
    def get_balance(self):
        """Abstract method to fetch account balance."""
        pass

