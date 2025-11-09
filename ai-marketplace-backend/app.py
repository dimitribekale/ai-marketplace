import os
import json
import logging
from web3 import Web3
from dotenv import load_dotenv
from flask import Flask, jsonify

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

if not RPC_URL or not CONTRACT_ADDRESS:
    logging.error("Error: RPC_URL or CONTRACT_ADDRESS not found in .env file.")
    exit()

try:
    with open("Marketplace.json") as f:
        abi_data = json.load(f)
        CONTRACT_ABI = abi_data["abi"]
except FileNotFoundError:
    logging.error("Error: Marketplace.json (ABI file) not found.")
    exit()

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    logging.error(f"Error: Could not connect to node at {RPC_URL}")
    exit()

logging.info(f"Connected to blockchain node at {RPC_URL}")
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def get_model_count():
    logging.info("Reading modelCount from contract...")
    try:
        count = contract.functions.modelCount().call()
        logging.info(f"Success! Current model count is: {count}")
        return count
    except Exception as e:
        logging.error(f"Error reading from contract: {e}", exc_info=True)

if __name__ == "__main__":
    get_model_count()
