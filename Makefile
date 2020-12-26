all: test

clean:
	rm -rf build dist *.egg-info/ .tox/ target/ venv/ instance/
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name '*~' -delete
	find . -name '*pb2_grpc.py' -delete
	find . -name '*pb2.py' -delete
	make --directory=frontend clean;

test:
	tox
	tox -e codechecks

codeformat:
	tox -e autoflake
	tox -e autopep8
	tox -e isort
	tox -e black

itest:
	./itests/run_itest.sh

coverage:
	tox -e coverage

mypy:
	tox -e mypy

run:
	tox -e run

.PHONY: all clean test itest coverage mypy run
