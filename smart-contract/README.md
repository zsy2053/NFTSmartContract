# Dependencies
- python3.11
    - web3
    - python-dotenv

# Setup environment
- create .env file in root directory
- add the following variables to .env file
    - PRIVATE_KEY
    - PROVIDER_API_ENDPOINT

# Usage

## Deploying ERC721 contract

Make sure UnspenderNFT.sol can be opened by `open("UnspenderNFT.sol")`
Run this python command: `python deploy.py --contract-name=UnspendNFT --contract-symbols=UNSPEND`
NOTE: This command has to be run SEQUENTIALLY.

if everything goes well, you should see the following output:

```json
{
    "account": "0xeF223bb983C224544F57B54E6BEeC16e655fec58",
    "nonce": 2,
    "gas_price": 2012551842,
    "gas_limit": 3223162,
    "signed_tx": "0x...",
    "tx_hash": "0x870b4e8515f4733c91424dd069e7647b51c66dc9c6306bce24a8222c8de145d2",
    "contract_address": "0x820445C5448b1AEA64e408B62aa40deA5ba10ac3",
    "status": "success"
}
```

Make sure to save the output for future use.

Exceptions:
1. TIMEOUT: if you see this error, retry the command with nonce value set to previous nonce value.
```json
{
    "account": "0xeF223bb983C224544F57B54E6BEeC16e655fec58",
    "nonce": 10,
    "gas_price": 1824355907,
    "gas_limit": 3223162,
    "signed_tx": "0x...",
    "tx_hash": "0xe79d8e5a368aa2cc3e25198622ec1797d480f80debf134a2a726918fcdef457b",
    "status": "timeout"
}
```
2. Insufficient Funds: Add more funds to your account. Retry the command with nonce value set to previous nonce value.
```json
{
    "account": "0x2588511c811254886CF6Ce6aCCdca9575fE58C6A",
    "nonce": 0,
    "gas_price": 1820201647,
    "gas_limit": 3223162,
    "signed_tx": "0x...",
    "status": "error",
    "error": "{'code': -32000, 'message': 'insufficient funds for gas * price + value'}"
}
```
