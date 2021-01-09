.PHONY: clean lint requirements build build_and_push

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
APP = senator-nlp-vote-prediction
PROFILE = jeremy_sagemaker
PYTHON_INTERPRETER = python3

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

build:
	sh ./build_local.sh

build_and_push:
	sh ./build_and_push.sh

local_server:
	docker run -i -t --rm --env-file=.env -p 8501:8501 --name=$(APP) "apps/$(APP)"
