PYTHON = python3
MAIN = main.py

.PHONY: run help clean

run:
	$(PYTHON) $(MAIN) ex.txt

help:
	@echo "Available targets:"
	@echo "  make run       Run the project with ex.txt"
	@echo "  make help      Show this help"
	@echo "  make clean     Remove Python cache files"

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
