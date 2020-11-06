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
- Start the squeak server with the `WEBADMIN_LOGIN_DISABLED` and `WEBADMIN_ALLOW_CORS` environment variables:
	```
	$ WEBADMIN_LOGIN_DISABLED=TRUE WEBADMIN_ALLOW_CORS=TRUE NETWORK=testnet docker-compose up
	```
- Start the frontend in dev mode with the `REACT_APP_SERVER_PORT` environment variable.
	```
	$ npm install
	$ REACT_APP_SERVER_PORT=12994 npm start
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
