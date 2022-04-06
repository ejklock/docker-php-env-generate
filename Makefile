SHELL := /bin/bash

.DEFAULT_GOAL := help

PWD ?= $$(pwd)
USERID ?= $$(id -u)

## Install Python requirements
requirements:
	pip install -r requirements.txt	

compile: ## Build executable
	make requirements && pyinstaller --onefile src/docker-dev-lamp-env.py

help: ## generate this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
