# frontend

## Build protos

- Install `protoc` and `protoc-gen-grpc-web`:
	https://github.com/grpc/grpc-web#code-generator-plugin
- Run `./build-protos.sh`

## Run in dev mode

- [Build protos](#build-protos)
- Edit **config.ini** and add the following configs in the `webadmin` section
	```
	login_disabled=true
	allow_cors=true
	```
- Start the squeak server.
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
