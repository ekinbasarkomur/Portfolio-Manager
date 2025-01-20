import os
import datetime
from dotenv import load_dotenv

load_dotenv()

DATA_DIR =  os.environ.get("DATA_DIR", str(os.getcwd()) + "/data")
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY", "")
BINANCE_SECRET_KEY = os.environ.get("BINANCE_SECRET_KEY", "")