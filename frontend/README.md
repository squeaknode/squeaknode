# frontend

## Run in dev mode

- Edit **config.ini** and add the following configs in the `webadmin` section
	```
	login_disabled=true
	allow_cors=true
	```
- Start the squeak server.
- Start the frontend in dev mode with the `REACT_APP_SERVER_PORT` environment variable.
	```
	$ REACT_APP_SERVER_PORT=12994 npm start
	```

## Build

- Install `protoc` and `protoc-gen-grpc-web`:
	https://github.com/grpc/grpc-web#code-generator-plugin

- Run `make-build.sh`

- Copy the generated `build` folder into `squeaknode/admin/webapp/static/`.
