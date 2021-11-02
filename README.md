# squeaknode

[![GitHub CI workflow](https://github.com/yzernik/squeaknode/actions/workflows/main.yml/badge.svg)](https://github.com/yzernik/squeaknode/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/yzernik/squeaknode/branch/master/graph/badge.svg?token=VV8WW3VR3Y)](https://codecov.io/gh/yzernik/squeaknode)

Node for [Squeak protocol](https://github.com/yzernik/squeak/blob/master/docs/PROTOCOL.md)

### Run a node:

#### Requirements
* a Bitcoin node
* an LND node
* Python 3.6 or later

#### Optional
* a Tor SOCKS5 proxy (you can open Tor Browser and run it in the background)

#### Steps
- Update the **config.ini** file and fill in the relevant sections to connect to your Bitcoin node and LND node:
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

	More information about [configs](docs/CONFIGURATION.md).

- Install squeaknode:
	```
	$ virtualenv venv
	$ source venv/bin/activate
	$ pip install -r requirements.txt
	$ pip install .
	```
- Start squeaknode:
 	```
	$ squeaknode --config config.ini
	```
- Go to http://localhost:12994/ and use the username/password in **config.ini** to log in.

## Test

### Unit tests:

#### Requirements
* tox

```
$ make test
```

### Integration tests:

#### Requirements
* docker-compose
* jq

```
$ make itest
```

## License

Distributed under the MIT License. See [LICENSE file](LICENSE).
