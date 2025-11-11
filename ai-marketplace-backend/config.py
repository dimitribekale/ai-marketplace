import os
import json
import logging
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
load_dotenv()


RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
LISTER_PRIVATE_KEY = os.getenv("LISTER_PRIVATE_KEY")

if not RPC_URL or not CONTRACT_ADDRESS or not LISTER_PRIVATE_KEY:
    logging.error("CRITICAL: Missing RPC_URL, CONTRACT_ADDRESS, or LISTER_PRIVATE_KEY in .env")
    raise EnvironmentError("Missing required environment variables")


def load_contract_abi(path="Marketplace.json"):
    try:
        with open(path) as f:
            abi_data = json.load(f)
            return abi_data["abi"]
    except FileNotFoundError as e:
        logging.error(f"Marketplace ABI file not found at {path}")
        raise e

CONTRACT_ABI = load_contract_abi("Marketplace.json")

try:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        raise ConnectionError("Web3 failed to connect")

    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    
    lister_account = Account.from_key(LISTER_PRIVATE_KEY)
    LISTER_ADDRESS = lister_account.address
    
    logging.info(f"Config loaded. Connected to {RPC_URL}")
    logging.info(f"Loaded contract at: {CONTRACT_ADDRESS}")
    logging.info(f"Loaded lister account: {LISTER_ADDRESS}")

except Exception as e:
    logging.critical(f"Failed to initialize config: {e}", exc_info=True)
    raise e
