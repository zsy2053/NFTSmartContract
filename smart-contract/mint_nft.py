# import web3
from web3 import Web3, HTTPProvider
from web3.exceptions import TimeExhausted
from dotenv import load_dotenv
import argparse
import os
import json


def mint_nft(
    contract_address, to_address, token_id, metadata_link, timeout=120, set_nonce=-1
):
    # create a result dictionary to return
    result = {}

    # Connect to the network
    w3 = Web3(HTTPProvider(os.getenv("PROVIDER_API_ENDPOINT")))

    # Load the contract ABI
    with open("UnspendNFT.json") as f:
        abi = json.load(f).get("abi")

    private_key = os.getenv("PRIVATE_KEY")
    account = w3.eth.account.from_key(private_key)
    result["account"] = account.address

    # get nonce
    try:
        nonce = w3.eth.get_transaction_count(account.address)
        if set_nonce != -1:
            nonce = set_nonce
        result["nonce"] = nonce
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        return result

    gas_price = w3.eth.gas_price
    result["gas_price"] = gas_price

    # create tx
    try:
        tx = w3.eth.contract(address=contract_address, abi=abi).functions.safeMint(
            Web3.to_bytes(hexstr=to_address), token_id, metadata_link
        )
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        return result

    # estimate gas limit
    try:
        gas_limit = tx.estimate_gas({"from": account.address}) * 2
        result["gas_limit"] = gas_limit
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        return result

    # Build and sign the transaction
    try:
        tx = tx.build_transaction(
            {
                "from": account.address,
                "nonce": nonce,
                "gas": gas_limit,
                "gasPrice": gas_price,
            }
        )
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        result["signed_tx"] = signed_tx.rawTransaction.hex()
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        return result

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
        w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        result["status"] = "success"
    except TimeExhausted as e:
        result["status"] = "timeout"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        return result

    return result


load_dotenv(override=True)

parser = argparse.ArgumentParser()
parser.add_argument("--contract-address", type=str, required=True)
parser.add_argument("--to-address", type=str, required=True)
parser.add_argument("--token-id", type=int, required=True)
parser.add_argument("--metadata-link", type=str, required=True)
parser.add_argument("--timeout", type=int, default=120)
parser.add_argument("--use-nonce", type=int, default=-1)
args = parser.parse_args()

result = mint_nft(
    args.contract_address,
    args.to_address,
    args.token_id,
    args.metadata_link,
    args.timeout,
    args.use_nonce,
)

print(json.dumps(result, indent=4))
