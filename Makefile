all: test

clean:
	rm -rf build dist *.egg-info/ .tox/ target/ venv/ instance/
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name '*~' -delete
	find . -name '*pb2_grpc.py' -delete
	find . -name '*pb2.py' -delete
	find . -name '*.pyi' -delete
	make --directory=frontend clean;

test: gen-protos
	tox

codeformat: gen-protos
	tox -e autoflake
	tox -e autopep8
	tox -e isort
	tox -e black

itest:
	./itests/run_itest.sh

coverage:
	tox -e coverage

mypy: gen-protos
	tox -e mypy

run: gen-protos
	tox -e run

gen-protos:
	tox -e setup

.PHONY: all clean test itest coverage mypy run
