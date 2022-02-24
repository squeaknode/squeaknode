# squeaknode

[![GitHub release](https://img.shields.io/github/release/squeaknode/squeaknode.svg)](https://github.com/squeaknode/squeaknode/releases)
[![GitHub CI workflow](https://github.com/squeaknode/squeaknode/actions/workflows/main.yml/badge.svg)](https://github.com/squeaknode/squeaknode/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/squeaknode/squeaknode/branch/master/graph/badge.svg?token=VV8WW3VR3Y)](https://codecov.io/gh/squeaknode/squeaknode)
[![Join the chat at https://gitter.im/squeaknode/squeaknode](https://badges.gitter.im/squeaknode/squeaknode.svg)](https://gitter.im/squeaknode/squeaknode?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A peer-to-peer status feed with posts unlocked by Lightning.

![Screenshot from 2021-11-11 04-17-41](docs/images/squeak-page.png)

Squeaknode allows you to create, view, buy, and sell squeaks.

A squeak is an immutable structure that:
* contains 280 utf-8 characters of text
* contains the hash of another squeak as a reply, if the squeak is a reply
* contains the height and block hash of the latest bitcoin block
* contains the public key of the author, and is signed by the author
* contains the public key of the recipient, if the text is end-to-end encrypted
* is encrypted until a lightning payment obtains the secret decryption key
* has a unique hash that is derived from its contents

The protocol is defined [here](https://github.com/yzernik/squeak/blob/master/docs/PROTOCOL.md).


## Installation

### Requirements
* a Bitcoin node
* an LND node
* Python 3.6 or later

#### Optional
* a Tor SOCKS5 proxy (you can open Tor Browser and run it in the background)

### Step 1. Create the configuration
> Update the **config.ini** file and fill in the relevant sections to connect to your Bitcoin node and LND node:

```
[node]
network=mainnet

[lnd]
host=localhost
tls_cert_path=~/.lnd/tls.cert
macaroon_path=~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon

[bitcoin]
rpc_host=localhost
rpc_port=8332
rpc_user=devuser
rpc_pass=devpass
zeromq_hashblock_port=28334

[tor]
proxy_ip=localhost
proxy_port=9150

[webadmin]
enabled=true
username=devuser
password=devpass
```

Add any other [configs](docs/configuration.md) that you need.

### Step 2. Install squeaknode:

```
pip install squeaknode
```

Or install from source

```
python3 -m venv venv
source venv/bin/activate
pip install .
```

### Step 3. Start squeaknode:

```
squeaknode --config config.ini
```

Go to http://localhost:12994/ and use the username/password in **config.ini** to log in.

## Test

### Unit tests:

#### Requirements
* tox

```
make test
```

### Integration tests:

#### Requirements
* docker-compose
* jq

```
make itest
```

## Release + Commit Verification

All releases and all maintainer commits as of January 5, 2022 are signed by key `D761F27D9B20BA52` (yzernik@gmail.com). The key can be found [in this repo](https://github.com/squeaknode/squeaknode/blob/master/PGP.txt) and [on the Squeaknode website](https://squeaknode.org/pgp.txt).

## Telegram

[Join our Telegram group!](https://t.me/squeaknode)

## License

Distributed under the MIT License. See [LICENSE file](LICENSE).
