all: clean build

clean:
	rm -rf build node_modules

rundev:
	./build-protos.sh
	npm install
	REACT_APP_SERVER_PORT=12994 npm start

build:
	./build-protos.sh
	npm install
	npm run build
	cp -r build/ ../squeaknode/admin/webapp/static/

.PHONY: all clean
