from web3 import Web3, HTTPProvider
from web3.exceptions import TimeExhausted
from dotenv import load_dotenv
import argparse
import os
import json


def deploy_contract(contract_name, contract_symbol, set_nonce=-1):
    result = {}

    # Connect to the network
    w3 = Web3(HTTPProvider(os.getenv("PROVIDER_API_ENDPOINT")))

    # Load the contract ABI
    with open("UnspendNFT.json") as f:
        abi = json.load(f).get("abi")

    # Load the contract bytecode
    with open("UnspendNFT.json") as f:
        bytecode = json.load(f).get("bytecode")

    # Create the contract in Python
    contract = w3.eth.contract(abi=abi, bytecode=bytecode).constructor(
        name=contract_name, symbol=contract_symbol
    )

    private_key = os.getenv("PRIVATE_KEY")
    account = w3.eth.account.from_key(private_key)
    result["account"] = account.address

    nonce = w3.eth.get_transaction_count(account.address)
    if set_nonce != -1:
        nonce = set_nonce
    result["nonce"] = nonce

    gas_price = w3.eth.gas_price
    result["gas_price"] = gas_price

    # estimate gas limit
    gas_limit = contract.estimate_gas() * 2
    result["gas_limit"] = gas_limit

    # Build a transaction that deploys the contract
    tx = contract.build_transaction(
        {
            "from": account.address,
            "nonce": nonce,
            "gas": gas_limit,
            "gasPrice": gas_price,
        }
    )

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    result["signed_tx"] = signed_tx.rawTransaction.hex()

    # Send the transaction
    try:
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        result["tx_hash"] = tx_hash.hex()
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        return result

    # Wait for the transaction to be mined
    # catch timeout error
    try:
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=15)
        result["contract_address"] = tx_receipt.contractAddress
        result["status"] = "success"
    except TimeExhausted as e:
        result["status"] = "timeout"

    return result


if __name__ == "__main__":
    # Load environment variables
    load_dotenv(override=True)

    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract-name", type=str, required=True)
    parser.add_argument("--contract-symbol", type=str, required=True)
    parser.add_argument("--use-nonce", type=int, default=-1)
    parser.add_argument("--publish-source", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    contract_name = args.contract_name
    contract_symbol = args.contract_symbol
    use_nonce = args.use_nonce

    result = deploy_contract(contract_name, contract_symbol, use_nonce)
    print(json.dumps(result, indent=4))
