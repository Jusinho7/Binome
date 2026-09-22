PYTHON := python3
VENV := venv
VENV_PYTHON := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip

MAP ?= maps/hard/03_ultimate_challenge.txt

.PHONY: install run debug clean lint lint-strict benchmark test

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PIP) install -r requirements.txt

run:
	$(VENV_PYTHON) main.py

debug:
	$(VENV_PYTHON) -m pdb main.py $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

lint:
	$(VENV_PYTHON) -m flake8 . --exclude=venv
	$(VENV_PYTHON) -m mypy . --exclude '^venv/' \
		--warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(VENV_PYTHON) -m flake8 . --exclude=venv
	$(VENV_PYTHON) -m mypy . --exclude '^venv/' --strict

benchmark:
	$(VENV_PYTHON) benchmark.py
