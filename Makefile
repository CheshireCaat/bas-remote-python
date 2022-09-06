.PHONY: tests
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
