# squeaknode

Node for Squeak protocol

## Run

### Run with docker:

##### Prerequisites
* docker
* docker-compose
* Enough disk space for the bitcoin blockchain

##### Steps
- Edit **docker/config.ini** to change any configs from the default.
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
- Create a **config.ini** file and fill in the relevant values:
	```
	[squeaknode]
	network=testnet
	price=100
	enable_sync=true

	[lnd]
	host=localhost

	[bitcoin]
	rpc_host=localhost
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

## Test

### Run unit tests:

```
$ make test
```

### Run integration tests:

```
$ make itest
```
