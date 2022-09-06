.PHONY: tests

tests_integration:
	poetry run python -m unittest tests.integration.functions_client_test

tests_types:
	poetry run python -m unittest tests.types.message_test
	poetry run python -m unittest tests.types.response_test
