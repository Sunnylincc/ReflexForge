PYTHON ?= python3

.PHONY: install test lint format demo-code demo-workflow run

install:
	$(PYTHON) -m pip install -e .[dev]

test:
	pytest -q

lint:
	ruff check src tests

format:
	ruff format src tests

demo-code:
	reflexforge demo code

demo-workflow:
	reflexforge demo workflow

run:
	reflexforge run --config configs/default.yaml
