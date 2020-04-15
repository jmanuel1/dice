.PHONY: typecheck init

typecheck:
	mypy dice.py

init:
	pip install -r requirements.txt
