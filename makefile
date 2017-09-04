VENV_DIR=$(CURDIR)/virt
DEV_VENV_DIR=$(CURDIR)/dev-virt
PYTHON=$(VENV_DIR)/bin/python
DEV_PYTHON=$(DEV_VENV_DIR)/bin/python


virt/:
	python3 -m venv $(VENV_DIR)
	$(PYTHON) -m pip install -r requirements.txt

dev-virt/:
	python3 -m venv $(DEV_VENV_DIR)
	$(DEV_PYTHON) -m pip install -r requirements.txt
	$(DEV_PYTHON) -m pip install -r dev-requirements.txt

watch-sass: ./dev-virt
	$(DEV_PYTHON) -mscss -o $(CURDIR)/public/css -w $(CURDIR)/scss

sportsteam.sqlite: ./dev-virt
	cd $(CURDIR)/scripts && $(DEV_PYTHON) populate_db.py
	mv $(CURDIR)/scripts/sportsteam.sqlite $(CURDIR)/sportsteam.sqlite

runserver: ./virt sportsteam.sqlite
	$(PYTHON) main.py

