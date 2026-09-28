PYTHON := python3
VENV := venv
VENV_PYTHON := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip
BENCH := benchmark.py
ARGS ?=

MAP ?= maps/hard/03_ultimate_challenge.txt

.PHONY: install run debug clean lint lint-strict benchmark

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PIP) install -e ".[dev]"

run:
	$(VENV_PYTHON) main.py $(ARGS)

debug:
	$(VENV_PYTHON) -m pdb main.py $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

lint:
	$(VENV_PYTHON) -m flake8 . --exclude=.venv,venv
	$(VENV_PYTHON) -m mypy . --exclude '(^|/)(\.venv|venv)/' \
		--warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(VENV_PYTHON) -m flake8 . --exclude=.venv,venv
	$(VENV_PYTHON) -m mypy . --exclude '(^|/)(\.venv|venv)/' --strict

benchmark:
	$(VENV_PYTHON) $(BENCH)
