# squeaknode

Node for Squeak protocol

## Run

### Run with docker:

##### Prerequisites
* docker
* docker-compose
* Enough disk space for the bitcoin blockchain

##### Steps
- Build and start docker-compose with the `NETWORK` environment variable set:
	```
	$ cd docker
	$ docker-compose build
	$ NETWORK=testnet docker-compose up
	```

### Run without docker:

##### Prerequisites
* A running bitcoin node
* A running lnd node
* Python3.6

##### Steps
- Create a **config.ini** file and fill in the relevant sections to connect to your bitcoin and lnd nodes:
	```
	[squeaknode]
	network=testnet
	price=100
	enable_sync=true

	[lnd]
	host=localhost
	port=9735
	rpc_port=10009

	[bitcoin]
	rpc_host=localhost
	rpc_port=18334
	rpc_user=devuser
	rpc_pass=devpass
	tls_cert_path=~/.lnd/tls.cert
	macaroon_path=~/.lnd/data/chain/bitcoin/testnet/admin.macaroon

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

## Test

### Run unit tests:

```
$ make test
```

### Run integration tests:

```
$ make itest
```
