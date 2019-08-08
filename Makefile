.PHONY: clean clean-build clean-pyc lint test setup help
SHELL := /bin/bash
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

setup-tests: ## install python project dependencies for tests
	pip install --upgrade pip wheel
	pip install --upgrade -r requirements.test.txt
	pip install -e .
	anyblok_createdb -c tests.cfg || anyblok_updatedb -c tests.cfg

setup-dev: ## install python project dependencies for development
	pip install --upgrade pip wheel
	pip install --upgrade -r requirements.dev.txt
	pip install -e .
	anyblok_createdb -c app.dev.cfg || anyblok_updatedb -c app.dev.cfg

clean-build: ## remove build artifacts
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 anyblok_product/

test: ## run anyblok pytest tests
	ANYBLOK_CONFIG_FILE=tests.cfg py.test -ra -vv -s -W ignore::DeprecationWarning anyblok_product/tests/

documentation: ## generate documentation
	anyblok_doc -c tests.cfg --doc-format RST --doc-output doc/source/apidoc.rst
	make -C doc/ html
	coverage html -d doc/build/html/coverage
