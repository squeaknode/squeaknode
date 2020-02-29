all: test

clean:
	rm -rf build dist *.egg-info/ .tox/ target/ venv/ instance/
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

test:
	tox

coverage:
	tox -e coverage

mypy:
	tox -e mypy

run:
	tox -e run

.PHONY: all clean test coverage mypy run
