# frontend

## Run in dev mode

- Start bitcoin-core and lnd in docker-compose:
	```
	cd docker
	docker-compose up
	```
- Start the backend with the `SQUEAKNODE_WEBADMIN_ENABLED`, `SQUEAKNODE_WEBADMIN_LOGIN_DISABLED`, and `SQUEAKNODE_WEBADMIN_ALLOW_CORS` environment variables:
	```
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt
	pip install .
	SQUEAKNODE_WEBADMIN_ENABLED=TRUE SQUEAKNODE_WEBADMIN_LOGIN_DISABLED=TRUE SQUEAKNODE_WEBADMIN_ALLOW_CORS=TRUE SQUEAKNODE_NETWORK=testnet squeaknode --config config.ini
	```
- Start the frontend in development mode:
	```
	cd frontend
	make rundev
	```

## Build for production

- Run the build command:
	```
	cd frontend
	make build
	```
