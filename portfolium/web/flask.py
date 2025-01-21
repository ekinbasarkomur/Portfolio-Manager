from portfolium.configs import *
from portfolium.utils.logger import setup_logger

import os
import json
from flask import Flask, request, jsonify

logger = setup_logger(LOGGER_NAME, LOG_LEVEL)
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Welcome to the Portfolium!"

# Route to return a JSON response
@app.route('/positions', methods=['GET'])
def positions():
    exchange = request.args.get('exchange')
    # Check if exchange exists in EXCHANGES
    if not exchange or exchange.lower() not in EXCHANGES:
        logger.info(f"Exchange '{exchange}' is not supported or missing")
        return jsonify({"error": f"Exchange '{exchange}' is not supported or missing"}), 400
    try:
        # Fetch positions from the selected exchange
        positions = EXCHANGES[exchange.lower()].get_positions()
        logger.info(f"Positions fetched from {exchange}: {positions}")
        return jsonify({"positions": positions})
    except Exception as e:
        # Handle any unexpected errors
        logger.error(f"An error occurred while fetching positions: {str(e)}")
        return jsonify({"error": f"An error occurred while fetching positions: {str(e)}"}), 500


# Route to accept and process POST data
@app.route('/balance', methods=['POST'])
def balance():
    data = request.json  # Get the JSON data from the request
    return jsonify({"received": data})

# 404 Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404


def print_request(request, path):
    print(f"Request Method: {request.method}")
    print(f"Request Path: /{path}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Query Params: {request.args}")
    print(f"Form Data: {request.form}")
    print(f"JSON Data: {request.json}")
    print(f"Body: {request.data.decode('utf-8')}")