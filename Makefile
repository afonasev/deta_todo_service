#
# VARIABLES
#

PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
POETRY = $(VENV)/bin/poetry
RUN = $(VENV)/bin/poetry run

CODE = app tests

#
# COMMON ACTIONS
#

.PHONY: help
help: ## Show the help
# print all strings starts with two # symbol from Makefile
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: init
init: ## Create python venv and install deps
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip poetry
	$(POETRY) install
	cp .env.example .env

.PHONY: shell
shell: ## run ipython shell
	$(RUN) ipython

#
# CVS ACTIONS
#

.PHONY: git_hooks
git_hooks: ## install git commit and pre-push hooks
	git init
	echo '#!/bin/bash\ncz check --commit-msg-file $$1' > .git/hooks/commit-msg
	echo '#!/bin/bash\nmake lint test' > .git/hooks/pre-push
	chmod +x .git/hooks/commit-msg
	chmod +x .git/hooks/pre-push

#
# CI ACTIONS
#

.PHONY: test
test: ## run tests
	@echo "\n********* RUN TESTS *********\n"
	$(RUN) pytest --cov=app tests $(args)

.PHONY: lint
lint: ## run linters
	@echo "\n********* RUN LINTERS *********\n"
	$(POETRY) check
	$(RUN) pflake8 $(CODE)
	$(RUN) mypy --no-error-summary $(CODE)
	find $(CODE) -name *.py -exec $(RUN) pyupgrade --py39-plus '{}' '+'
	$(RUN) docformatter --check --recursive $(CODE)
	$(RUN) autoflake --check --recursive \
		--expand-star-imports \
		--ignore-init-module-imports \
		--remove-all-unused-imports \
		--remove-duplicate-keys \
		--remove-unused-variables $(CODE)
	$(RUN) pytest --dead-fixtures --dup-fixtures tests

.PHONY: pretty
pretty: ## run formatters
	@echo "\n********* RUN FORMATTERS *********\n"
	find $(CODE) -name *.py -exec $(RUN) pyupgrade --py39-plus --exit-zero-even-if-changed '{}' '+'
	$(RUN) docformatter --in-place --recursive $(CODE)
	$(RUN) isort $(CODE)
	$(RUN) black --quiet $(CODE) > /dev/null 2>&1
	$(RUN) unify --in-place --recursive $(CODE)
	$(RUN) autoflake --in-place --recursive \
		--expand-star-imports \
		--ignore-init-module-imports \
		--remove-all-unused-imports \
		--remove-duplicate-keys \
		--remove-unused-variables $(CODE)

#
# DEPLOY ACTIONS
#

.PHONY: run
run: ## run local server on 0.0.0.0:8080
	$(RUN) uvicorn main:app --reload --no-access-log --host 0.0.0.0 --port 8080

.PHONY: create_requirements
create_requirements: ## create requirements.txt for deta deploy
	$(POETRY) export --without-hashes > requirements.txt

.PHONY: deploy
deploy: ## deploy app to deta
	deta deploy

#
# APPLICATION ACTIONS
#
