# development

### Run in development mode:

#### Background services

- Start the required background services in docker:
	```
	$ cd docker
	$ docker-compose build
	$ docker-compose up
	```
- You may need to change the permissions of the `~/.lnd` directory after docker containers start:
	```
	$ sudo chmod -R 755 ~/.lnd/
	```

#### Squeaknode backend

- Install squeaknode:
	```
	$ virtualenv venv
	$ source venv/bin/activate
	$ pip install -r requirements.txt
	$ python setup.py install
	```
- Run squeaknode with authentication disabled:
	```
	$ SQUEAKNODE_WEBADMIN_ENABLED=TRUE SQUEAKNODE_WEBADMIN_LOGIN_DISABLED=TRUE SQUEAKNODE_WEBADMIN_ALLOW_CORS=TRUE SQUEAKNODE_NETWORK=testnet squeaknode --config config.ini
	```

To use a tor proxy, include the following environment variables:
	```
	$ SQUEAKNODE_NODE_TOR_PROXY_IP=127.0.0.1 SQUEAKNODE_NODE_TOR_PROXY_PORT=9150
	```


#### Squeaknode frontend

- Install `protoc-gen-grpc-web` (https://github.com/grpc/grpc-web#code-generator-plugin)
- Run the frontend react app in dev mode:
	```
	$ cd frontend
	$ make rundev
	```
