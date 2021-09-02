# squeaknode

Node for Squeak protocol

### Run a node:

#### Requirements
* a bitcoin node
* an LND node
* Python 3.6 or later

#### Steps
- Update the **config.ini** file and fill in the relevant sections to connect to your bitcoin and lnd nodes:
	```
	[core]
	network=testnet

	[lnd]
	host=localhost
	external_host=lnd_server
	tls_cert_path=~/.lnd/tls.cert
	macaroon_path=~/.lnd/data/chain/bitcoin/testnet/admin.macaroon

	[bitcoin]
	rpc_host=localhost
	rpc_port=18332
	rpc_user=devuser
	rpc_pass=devpass

	[webadmin]
	enabled=true
	username=devuser
	password=devpass
	```
- Install squeaknode:
	```
	$ pip install -r requirements.txt
	$ python setup.py install
	```

- Start the squeaknode:
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
