import logging
from config import w3, contract, LISTER_ADDRESS, LISTER_PRIVATE_KEY

def get_model_count_from_chain():
    """
    Reads the modelCount from the contract.
    Returns:
        int: The current model count.
    Raises:
        Exception: If the contract call fails.
    """
    logging.info("Service: Reading modelCount...")
    try:
        count = contract.functions.modelCount().call()
        logging.info(f"Service: modelCount is {count}")
        return count
    except Exception as e:
        logging.error(f"Service Error: Failed to read modelCount: {e}", exc_info=True)
        # Re-raise the exception so the web layer can handle it
        raise Exception("Contract call failed")
    
def list_new_model(name: str, price: int, url:str):
    """
    Builds, signs, and sends a transaction to list a new model.
    Returns:
        dict: A dictionary with the transaction receipt.
    Raises:
        Exception: If the transaction fails.
    """
    logging.info(f"Service: Listing new model: {name}")
    try:
        nonce = w3.eth.get_transaction_count(LISTER_ADDRESS)

        # Build the transaction
        transaction = contract.function.listModel(name, price, url).build_transaction({
            'from': LISTER_ADDRESS,
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
        })

        # Sign the transaction
        signed_transaction = w3.eth.account.sign_transaction(transaction, LISTER_PRIVATE_KEY)

        # Send the transaction
        logging.info("Service: Sending transaction...")
        transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # Wait for the receipt
        receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
        logging.info(f"Service: Transaction mined! Block: {receipt.blockNumber}")

        return {
            'transaction_hash': transaction_hash.hex(),
            'block_number': receipt.blockNumber,
            'gas_used': receipt.gasUsed
        }
    
    except Exception as e:
        logging.error(f"Service Error: Failed to list model: {e}", exc_info=True)
        raise Exception("Transaction failed")