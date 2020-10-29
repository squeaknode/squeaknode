# squeaknode

Node for Squeak protocol

## Run

### Run with docker:

- Edit **docker/config.ini** to change any configs
- Start the squeak server:
	```
	$ cd docker
	$ docker-compose build
	$ docker-compose up
	```

### Run without docker:

- Create a **config.ini** file and fill in the relevant values:
	```
	[squeaknode]
	network=testnet
	price=<YOUR_SELLING_PRICE_IN_SATOSHIS>
	max_squeaks_per_address_per_hour=<YOUR_RATE_LIMIT>

	[lnd]
	host=<YOUR_LND_HOST>
	external_host=<YOUR_LND_HOST>
	port=9735
	rpc_port=10009
	tls_cert_path=/root/.lnd/tls.cert
	macaroon_path=/root/.lnd/data/chain/bitcoin/testnet/admin.macaroon

	[bitcoin]
	rpc_host=btcd
	rpc_port=18334
	rpc_user=devuser
	rpc_pass=devpass

	[server]
	rpc_host=0.0.0.0
	rpc_port=8774

	[admin]
	rpc_host=0.0.0.0
	rpc_port=8994
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
