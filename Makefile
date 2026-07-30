CONFIG ?= config.txt

.PHONY: install run debug clean lint lint-strict

install:
	pip install --break-system-packages -q flake8 mypy

run:
	python3 a_maze_ing.py $(CONFIG)

debug:
	python3 -m pdb a_maze_ing.py $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
