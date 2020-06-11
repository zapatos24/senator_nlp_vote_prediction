.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3 sync_models_to_s3 build build_and_push

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = senator-nlp-vote-prediction
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


## Upload Data to S3
sync_data_to_s3:
ifeq (default,$(PROFILE))
	aws s3 sync data/ s3://$(BUCKET)/data/
else
	aws s3 sync data/ s3://$(BUCKET)/data/ --profile $(PROFILE)
endif


## Download Data from S3
sync_data_from_s3:
ifeq (default,$(PROFILE))
	aws s3 sync s3://$(BUCKET)/data/ data/
else
	aws s3 sync s3://$(BUCKET)/data/ data/ --profile $(PROFILE)
endif


## Upload XGBoost Models to S3
sync_models_to_s3:
ifeq (default,$(PROFILE))
	aws s3 sync model_artifacts/ s3://$(BUCKET)/model_artifacts/
else
	aws s3 sync model_artifacts/ s3://$(BUCKET)/model_artifacts/ --profile $(PROFILE)
endif

build:
	sh ./build_local.sh

build_and_push:
	sh ./build_and_push.sh


