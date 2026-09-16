PYTHON = python3
MAIN = main.py
FILE = maps/easy/01_linear_path.txt

.PHONY: run help clean

run:
	$(PYTHON) $(MAIN) $(FILE)

install:
	$(PYTHON) -m pip install -r requirements.txt

help:
	@echo "Available targets:"
	@echo "  make run       Run the project with the default map"
	@echo "  make help      Show this help"
	@echo "  make clean     Remove Python cache files"

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
