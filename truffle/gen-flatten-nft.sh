#!/bin/sh

# install truffle-flattener
npm install -g truffle-flattener

# This script generates a flattened version of the NFT contract.
echo "// SPDX-License-Identifier: MIT" > unspend-nft-flattened.sol
truffle-flattener contracts/unspend-nft.sol | grep -v "SPDX-License-Identifier" >> unspend-nft-flattened.sol
