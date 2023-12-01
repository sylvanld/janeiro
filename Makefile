
VENV?=venv

##@ Targets used to work on package

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

requires-venv: # Makes decorated target fail if virtualenv does not exists
	@if [ ! -d "$(VENV)" ]; then echo "You need to run 'make install' first"; exit 1; fi

$(VENV): # Create virtualenv if not exists
	virtualenv -p python3 $(VENV)

install: $(VENV) ## Install dev. dependencies in a virtual env
	$(VENV)/bin/pip install -e .[dev]

format: requires-venv ## Apply formatting to package source code
	$(VENV)/bin/isort janeiro tests/
	$(VENV)/bin/black janeiro tests/

test: requires-venv ## Run package unit tests
	$(VENV)/bin/python -m pytest -vvv tests
