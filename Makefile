PYTHON  ?= python3
PIP     ?= $(PYTHON) -m pip
CONFIG  ?= config.txt

.PHONY: install run debug clean lint lint-strict package

install:
	$(PIP) install --break-system-packages -r requirements-dev.txt

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy . --strict

package:
	$(PYTHON) -m build --wheel -o dist
	cp dist/mazegen-*.whl .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .pytest_cache build mazegen.egg-info dist
