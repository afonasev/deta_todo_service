#
# Variables
#

PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
POETRY = $(VENV)/bin/poetry
CODE = app tests

#
## COMMON ACTIONS
#

.PHONY: help
help: ## Show the help
# print all strings starts with "##" from Makefile
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: init
init: ## Create python venv and install deps
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip poetry
	$(POETRY) install

.PHONY: shell
shell: ## run ipython shell
	ipython

#
## CVS ACTIONS
#

.PHONY: bump_version
bump_version: ## bump new version
	cz bump --check-consistency --annotated-tag

.PHONY: git_hooks
git_hooks: ## install git commit and pre-push hooks
	git init
	echo '#!/bin/bash\ncz check --commit-msg-file $$1' > .git/hooks/commit-msg
	echo '#!/bin/bash\ndocker compose run --rm dev make lint test' > .git/hooks/pre-push
	chmod +x .git/hooks/commit-msg
	chmod +x .git/hooks/pre-push

#
## CI ACTIONS
#

.PHONY: test
test: ## run tests
	@echo "\n********* RUN TESTS *********\n"
	pytest --cov=app tests $(args)

.PHONY: lint
lint: ## run linters
	@echo "\n********* RUN LINTERS *********\n"
	pflake8 $(CODE)
	mypy --no-error-summary $(CODE)
	find $(CODE) -name *.py -exec pyupgrade --py310-plus '{}' '+'
	docformatter --check --recursive $(CODE)
	autoflake --check --recursive \
		--expand-star-imports \
		--ignore-init-module-imports \
		--remove-all-unused-imports \
		--remove-duplicate-keys \
		--remove-unused-variables $(CODE)
	pytest --dead-fixtures --dup-fixtures tests

.PHONY: pretty
pretty: ## run formatters
	@echo "\n********* RUN FORMATTERS *********\n"
	find $(CODE) -name *.py -exec pyupgrade --py310-plus --exit-zero-even-if-changed '{}' '+'
	docformatter --in-place --recursive $(CODE)
	isort $(CODE)
	black --quiet $(CODE) > /dev/null 2>&1
	unify --in-place --recursive $(CODE)
	autoflake --in-place --recursive \
		--expand-star-imports \
		--ignore-init-module-imports \
		--remove-all-unused-imports \
		--remove-duplicate-keys \
		--remove-unused-variables $(CODE)

#
## APPLICATION ACTIONS
#
