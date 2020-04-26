.PHONY: install
install:
	pip install -r requirements-dev.txt && \
	pre-commit install

.PHONY: test
test:
	python -m pytest --cov=app

.PHONY: run
run:
	uvicorn --reload app:app
