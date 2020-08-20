# squeakserver

Server for Squeak protocol

## Test

### Run unit tests:

```
$ make test
```

### Run integration tests:

```
$ make itest
```

## Run

### Run with docker:

- Edit **docker/config.ini** to use your external IP address for `external_host`
- Start the squeak server:
	```
	$ cd docker
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
- Run the **createdb.sql** script on the postgres server to initialize the database.
- Install the server requirements:
	```
	$ pip3 install -r requirements.txt
	$ cp proto/* squeakserver/proto/
	$ python3 setup.py install
	```
- Start the squeak server:
 	```
	$ runsqueakserver --config config.ini run-server
	```
