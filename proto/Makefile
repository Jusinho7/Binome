PYTHON  ?= python3
PIP     ?= pip3
MAP     ?= maps/example_subject.txt

MYPY_FLAGS := --warn-return-any --warn-unused-ignores --ignore-missing-imports \
              --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint lint-strict test

install:
	$(PIP) install --break-system-packages -r requirements-dev.txt

run:
	$(PYTHON) -m fly_in.main $(MAP)

debug:
	$(PYTHON) -m pdb -m fly_in.main $(MAP)

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	flake8 .
	mypy . $(MYPY_FLAGS)

lint-strict:
	flake8 .
	mypy . --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .pytest_cache
