SHELL := /bin/bash
CURR_DIR := $(SHELL pwd)

install: install_cscout install_tokenizer
	python3 setup.py install

install_cscout:
	cd cscout/ && $(MAKE) && $(MAKE) install

install_tokenizer:
	cd tokenizer && $(MAKE) && $(MAKE) install

install_venv: 
	virtualenv -p python3 sade_env
	source sade_env/bin/activate
	pip3 install pip --upgrade
	pip3 install -r requirements.txt
	$(MAKE) install

test_all:
	pytest tests/
