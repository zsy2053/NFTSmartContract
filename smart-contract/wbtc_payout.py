# import web3
from web3 import Web3, HTTPProvider
from web3.exceptions import TimeExhausted
from dotenv import load_dotenv
import argparse
import os
import json
import requests


def get_wbtc_conversion_rate(usd_amount: float):
    coinbase_endpoint = os.getenv("COINBASE_API_ENDPOINT")
    response = requests.get(coinbase_endpoint)
    rate = response.json().get("data").get("amount")
    wbtc_amount = usd_amount / float(rate)
    return (rate, int(wbtc_amount * 10**8))


def wbtc_payout(recipient, amount: float, timeout=120, set_nonce=-1):
    # create a result dictionary to return
    result = {}

    try:
        # Connect to the network
        w3 = Web3(HTTPProvider(os.getenv("PROVIDER_API_ENDPOINT")))

        # Load the contract ABI
        with open("wbtc.abi") as f:
            abi = f.read()

        private_key = os.getenv("PRIVATE_KEY")
        account = w3.eth.account.from_key(private_key)
        result["account"] = account.address

        # get nonce
        nonce = w3.eth.get_transaction_count(account.address)
        if set_nonce != -1:
            nonce = set_nonce
        result["nonce"] = nonce

        gas_price = w3.eth.gas_price
        result["gas_price"] = gas_price

        # get wbtc contract address
        wbtc_address = os.getenv("WBTC_CONTRACT_ADDRESS")
        wbtc_address = Web3.to_bytes(hexstr=wbtc_address)

        # compute wbtc amount
        conversion_rate, wbtc_amount = get_wbtc_conversion_rate(amount)
        result["wbtc_amount"] = wbtc_amount
        result["conversion_rate"] = conversion_rate

        # create tx
        tx = w3.eth.contract(address=wbtc_address, abi=abi).functions.transfer(
            recipient=recipient, amount=wbtc_amount
        )

        # estimate gas limit
        gas_limit = tx.estimate_gas({"from": account.address}) * 2
        result["gas_limit"] = gas_limit

        # build tx
        tx = tx.build_transaction(
            {
                "from": account.address,
                "nonce": nonce,
                "gas": gas_limit,
                "gasPrice": gas_price,
            }
        )

        # sign tx
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        result["signed_tx"] = signed_tx.rawTransaction.hex()

        # send tx
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        result["tx_hash"] = tx_hash.hex()

        # wait for tx to be mined
        w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        result["status"] = "success"

    except TimeExhausted as e:
        result["status"] = "timeout"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--recipient", type=str, required=True)
    parser.add_argument("--amount", type=float, required=True)
    args = parser.parse_args()

    load_dotenv(override=True)
    result = wbtc_payout(args.recipient, args.amount)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
