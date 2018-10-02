SHELL := /bin/bash

install: 
	python3 setup.py install

install_venv: 
	virtualenv -p python3 sade_env
	source sade_env/bin/activate
	pip3 install pip3 --upgrade
	pip3 install -r requirements.txt
	$(MAKE) install