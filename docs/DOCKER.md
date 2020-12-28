# Running bitcoin-core and LND with Docker

If you don't already have your own bitcoin node and lightning node, you can use docker-compose to launch new ones.

##### Steps
- Build and start docker-compose:
	```
	$ cd docker
	$ docker-compose build
	$ docker-compose up
	```
- If you want to use testnet, run the normal `up` command:
	```
	$ docker-compose up
	```
- If you want to use mainnet, run with the `docker-compose.mainnet.yml` override file:
	```
	$ docker-compose -f docker-compose.yml -f docker-compose.mainnet.yml up
	```
