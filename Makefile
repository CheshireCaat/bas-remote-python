.PHONY: tests tests_integration tests_types create_requirements build
.DEFAULT_GOAL := tests

tests:
	$(MAKE) tests_integration
	$(MAKE) tests_types

tests_integration:
	poetry run python -m unittest tests.integration.functions_client_test
	poetry run python -m unittest tests.integration.functions_thread_test

tests_types:
	poetry run python -m unittest tests.types.message_test
	poetry run python -m unittest tests.types.response_test

build:
	python setup.py build

clean:
	rm -rf ./build || echo ""

create_requirements:
	poetry export --without-hashes --without-urls -f requirements.txt --output requirements.txt
