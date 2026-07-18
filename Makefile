PY ?= uv run python

.PHONY: all numbers figures pdf check clean

all: numbers figures pdf check

numbers:
	$(PY) scripts/aggregate.py

figures:
	$(PY) scripts/make_figures.py
	$(PY) scripts/make_qualitative.py

pdf:
	latexmk -pdf -interaction=nonstopmode main.tex

check:
	$(PY) scripts/check_citations.py

clean:
	latexmk -C main.tex
