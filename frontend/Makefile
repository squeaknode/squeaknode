all: clean build

clean:
	rm -rf build node_modules

rundev:	gen-protos
	npm install
	REACT_APP_SERVER_PORT=12994 npm start

build:  gen-protos
	npm install
	npm run build
	cp -r build/ ../squeaknode/admin/webapp/static/

gen-protos:
	./build-protos.sh

.PHONY: all clean rundev build gen-protos
