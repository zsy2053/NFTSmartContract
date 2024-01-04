# README

## Description
This repo contains helper scripts for interacting with nft.storage.

## Dependencies
- nodejs 18
- yarn
    - dotenv
    - nft.storage

## Setup
- install nodejs 18 (NOTE: don't use nodejs 19 or it will break)
- install yarn
- install dependencies
    - `yarn install dotenv nft.storage`
- create a .env file in the root directory
    - `echo NFT_STORAGE_API_KEY={your api key} > .env`

## Usage

### upload.js

Script is used to upload an image to nft.storage

Command: `node upload.js {path to image file}`

Example:
```plaintext
root@a52b4c9c6b34:/workdir# node upload.mjs image.png 
{ cid: 'bafkreihv6axkobbobv5lnskpmysnoifaxp3ei7y7wdlydoqvs65yqs2rxy' }
```

Exceptions:
1. Timed out waiting for pinning
    If you get this error, it means that the image was uploaded to nft.storage but it was not pinned. You can wait a few minutes and try again.
2. Request failed with status code 429
    Rate limit exceeded. You can try again in 1 minute.
3. 401 Unauthorized or 403 Forbidden
    Invalid API key. Check your .env file.


