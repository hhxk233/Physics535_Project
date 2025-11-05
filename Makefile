PYTHON ?= python
VENV ?= .venv
VENV_PY := $(VENV)/Scripts/python
VENV_PIP := $(VENV)/Scripts/pip
ALT_VENV_PY := $(VENV)/bin/python
ALT_VENV_PIP := $(VENV)/bin/pip

.PHONY: setup test figs gif

setup:
	$(PYTHON) -m venv $(VENV)
	-$(VENV_PY) -m pip install --upgrade pip || $(ALT_VENV_PY) -m pip install --upgrade pip
	-$(VENV_PIP) install -e . || $(ALT_VENV_PIP) install -e .

test:
	$(PYTHON) -m pytest -q

figs:
	$(PYTHON) -m src.cli.make_figs --panels all

gif:
	$(PYTHON) -m src.viz.gifs

