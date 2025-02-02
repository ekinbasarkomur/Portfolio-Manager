import os
import datetime
import logging
from dotenv import load_dotenv

load_dotenv()

DATA_DIR =  os.environ.get("DATA_DIR", str(os.getcwd()) + "/data")

# Binance API keys
############################################
BINANCE_EXCHANGE="binance"
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY", "")
BINANCE_SECRET_KEY = os.environ.get("BINANCE_SECRET_KEY", "")
############################################


# OKX API keys
############################################
OKX_EXCHANGE="okx"
OKX_API_KEY = os.environ.get("OKX_API_KEY", "")
OKX_SECRET_KEY = os.environ.get("OKX_SECRET_KEY", "")
OKX_PASSPHRASE = os.environ.get("OKX_PASSPHRASE", "")
############################################


# Logger setup
############################################
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOGGER_NAME = "PortfoliumLogger"

LOG_DIR = os.path.join(DATA_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"app_{datetime.datetime.now().strftime('%Y%m%d')}.log")

#logger = logging.getLogger(LOGGER_NAME)
############################################