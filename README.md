# squeaknode

Node for [Squeak protocol](https://github.com/yzernik/squeak/blob/master/docs/PROTOCOL.md)

### Run a node:

#### Requirements
* a bitcoin node
* an LND node
* Python 3.6 or later
* a Tor SOCKS5 proxy (you can open Tor Browser and run it in the background)
* libpq-dev (`sudo apt install libpq-dev` on ubuntu)

#### Steps
- Update the **config.ini** file and fill in the relevant sections to connect to your bitcoin node and lnd node:
	```
	[node]
	network=mainnet
	tor_proxy_ip=localhost
	tor_proxy_port=9150

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

	[webadmin]
	enabled=true
	username=devuser
	password=devpass
	```
- Install squeaknode:
	```
	$ virtualenv venv
	$ source venv/bin/activate
	$ pip install -r requirements.txt
	$ python setup.py install
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
