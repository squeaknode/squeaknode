# frontend

## Build protos

- Install `protoc` and `protoc-gen-grpc-web`:
	https://github.com/grpc/grpc-web#code-generator-plugin
	```
	curl -sSL https://github.com/protocolbuffers/protobuf/releases/download/v3.12.2/protoc-3.12.2-linux-x86_64.zip -o protoc.zip && \
		unzip -qq protoc.zip && \
		cp ./bin/protoc /usr/local/bin/protoc

	curl -sSL https://github.com/grpc/grpc-web/releases/download/1.2.1/protoc-gen-grpc-web-1.2.1-linux-x86_64 -o /usr/local/bin/protoc-gen-grpc-web && \
		chmod +x /usr/local/bin/protoc-gen-grpc-web
	```
- Run `./build-protos.sh`

## Run in dev mode

- [Build protos](#build-protos)
- Start bitcoin-core and lnd in docker-compose:
	```
	$ cd ../docker
	$ docker-compose up
	```
- Start the squeak node backend with the `SQUEAKNODE_WEBADMIN_ENABLED`, `SQUEAKNODE_WEBADMIN_LOGIN_DISABLED`, and `SQUEAKNODE_WEBADMIN_ALLOW_CORS` environment variables:
	```
	$ cd ..
	$ virtualenv venv
	$ source venv/bin/activate
	$ pip install -r requirements.txt
	$ python setup.py install
	$ SQUEAKNODE_WEBADMIN_ENABLED=TRUE SQUEAKNODE_WEBADMIN_LOGIN_DISABLED=TRUE SQUEAKNODE_WEBADMIN_ALLOW_CORS=TRUE SQUEAKNODE_NETWORK=testnet runsqueaknode run-server
	```
- Run the frontend in development mode:
	```
	$ make rundev
	```

## Build for production

- [Build protos](#build-protos)
- Make the build:
	```
	$ npm install
	$ npm run build
	```
- Copy the generated `build` folder into `squeaknode/admin/webapp/static/`.
	```
	$ cp -r build/ ../squeaknode/admin/webapp/static/
	```
Or run the following instead:
	```
	$ make build
	```
