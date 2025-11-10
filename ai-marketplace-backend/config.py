import os
import json
import logging
from dotenv import load_dotenv
from web3 import Web3


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
    exit()


try:
    with open("Marketplace.json") as f:
        abi_data = json.load(f)
        CONTRACT_ABI = abi_data["abi"]
except FileNotFoundError:
    logging.error("CRITICAL: Marketplace.json (ABI file) not found.")
    exit()


try:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        raise ConnectionError("Web3 failed to connect")

    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    
    lister_account = Web3.to_account(LISTER_PRIVATE_KEY)
    LISTER_ADDRESS = lister_account.address
    
    logging.info(f"Config loaded. Connected to {RPC_URL}")
    logging.info(f"Loaded contract at: {CONTRACT_ADDRESS}")
    logging.info(f"Loaded lister account: {LISTER_ADDRESS}")

except Exception as e:
    logging.critical(f"Failed to initialize config: {e}", exc_info=True)
    exit()