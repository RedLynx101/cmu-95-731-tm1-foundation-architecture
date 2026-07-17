.PHONY: install run test lint check smoke review diagram

install:
	python -m pip install -e ".[dev]"

run:
	python -m uvicorn app.main:app --app-dir src --reload --host 0.0.0.0 --port 8000

test:
	python -m pytest

lint:
	python -m ruff check .

check: lint test

smoke:
	python scripts/smoke_test.py

review: check smoke diagram

diagram:
	python scripts/render_architecture.py
