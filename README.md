# squeaknode

Node for Squeak protocol

### Run a node:

#### Requirements
* a bitcoin node
* an LND node
* Python 3.7 or later

If you don't already have a bitcoin node or lightning node, you can [follow the instructions](docs/DOCKER.md) follow the instructions here to launch them in Docker.

#### Steps
- Create a **config.ini** file and fill in the relevant sections to connect to your bitcoin and lnd nodes:
	```
	[squeaknode]
	network=testnet
	price_msat=1000000
	sync_interval_s=10

	[lnd]
	host=localhost
	port=9735
	rpc_port=10009
	tls_cert_path=~/.lnd/tls.cert
	macaroon_path=~/.lnd/data/chain/bitcoin/testnet/admin.macaroon

	[bitcoin]
	rpc_host=localhost
	rpc_port=18334
	rpc_user=devuser
	rpc_pass=devpass

	[webadmin]
	enabled=true
	username=devuser
	password=devpass
	```
- Install squeaknode:
	```
	$ pip install squeaknode
	```
	or
	```
	$ python setup.py install
	```

- Start the squeak server:
 	```
	$ runsqueaknode --config config.ini run-server
	```
- Go to http://localhost:12994/ and use the username/password in **config.ini** to log in.

## Test

### Run unit tests:

```
$ make test
```

### Run integration tests:

```
$ make itest
```
