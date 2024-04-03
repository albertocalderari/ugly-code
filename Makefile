include $(shell Makefile.venv)

.PHONY: venv
venv:
	pip3 install Makefile.venv

.PHONY: install
install:
	pip3 install -r ./requirements.txt

.PHONY: install-dev
install-dev:
	pip3 install --upgrade -r ./requirements.txt --no-compile


.PHONY: test
test:
	pytest -vv --disable-warnings tests/

.PHONY: coverage
coverage: environment-variable-default venv
	rm -f .coverage
	rm -f coverage.xml
	$(VENV)/python -m pip install --upgrade -r .requirements/dev.txt --no-compile
	$(VENV)/python -m coverage run -m pytest tests/ --disable-warnings
	$(VENV)/python -m coverage report -m --omit=tests
	$(VENV)/python -m coverage xml
	$(VENV)/python -m coverage html
	$(VENV)/python -m pytype . -j 10 --none-is-not-bool

.PHONY: type-check
type-check: ## typechecks your file for you
	pytype . -j 10 --none-is-not-bool

.PHONY: run
run:
	uvicorn main:app --reload

.PHONY: help
help: ## Show make target documentation
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)
