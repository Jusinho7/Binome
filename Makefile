PYTHON ?= python3
CONFIG ?= config.txt
VENV_DIR ?= .venv

VENV_PYTHON = $(VENV_DIR)/bin/python3
VENV_PIP = $(VENV_DIR)/bin/pip

.PHONY: install run debug clean lint lint-strict package

$(VENV_DIR)/bin/activate:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_PIP) install --upgrade pip -q

install: $(VENV_DIR)/bin/activate
	$(VENV_PIP) install -r requirements-dev.txt

run: $(VENV_DIR)/bin/activate
	$(VENV_PYTHON) a_maze_ing.py $(CONFIG)

debug: $(VENV_DIR)/bin/activate
	$(VENV_PYTHON) -m pdb a_maze_ing.py $(CONFIG)

lint: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/flake8 --exclude=$(VENV_DIR) .
	$(VENV_DIR)/bin/mypy --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --exclude $(VENV_DIR) .

lint-strict: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/flake8 --exclude=$(VENV_DIR) .
	$(VENV_DIR)/bin/mypy . --strict --exclude $(VENV_DIR)

package: $(VENV_DIR)/bin/activate
	$(VENV_PYTHON) -m build --wheel -o dist
	cp dist/mazegen-*.whl .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .pytest_cache build mazegen.egg-info dist