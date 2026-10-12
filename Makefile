SHELL := /bin/bash

.PHONY:
	run \
	test \
	test-with-coverage \
	test-with-coverage-and-reports \
	test-unit \
	test-unit-with-coverage \
	test-unit-with-coverage-and-reports \
	test-conformance \
	test-structure \
	compile-requirements \
	check-requirements

# * -------------------------------- *

run:
	@uv run python -m src.host.main

# * -------------------------------- *

test:
	@uv run python -m pytest tests

test-with-coverage:
	@uv run python -m pytest tests --cov=src; \
	status=$$?; \
	rm -f .coverage; \
	exit $$status

test-with-coverage-and-reports:
	@uv run python -m pytest tests --cov=src --cov-report=term-missing --cov-report=xml; \
	status=$$?; \
	rm -f .coverage; \
	exit $$status

test-unit:
	@uv run python -m pytest tests/unit

test-unit-with-coverage:
	@uv run python -m pytest tests/unit --cov=src; \
	status=$$?; \
	rm -f .coverage; \
	exit $$status

test-unit-with-coverage-and-reports:
	@uv run python -m pytest tests/unit --cov=src --cov-report=term-missing --cov-report=xml; \
	status=$$?; \
	rm -f .coverage; \
	exit $$status

test-conformance:
	@uv run python -m pytest tests/conformance

test-structure:
	@SRC=$$(cd src && find . -type f -name "*.py" ! -name "__init__.py" | sed 's|^\./||' | sort); \
	TESTS=$$(cd tests/unit && find . -type f -name "test_*.py" | sed 's|^\./||; s|/test_|/|; s|^test_||' | sort); \
	MISSING_TESTS=$$(comm -23 <(echo "$$SRC") <(echo "$$TESTS") | grep -v '^$$'); \
	MISSING_SRC=$$(comm -13 <(echo "$$SRC") <(echo "$$TESTS") | grep -v '^$$'); \
	if [ -z "$$MISSING_TESTS" ] && [ -z "$$MISSING_SRC" ]; then \
		echo 'Test structure up to date.'; \
	else \
		echo 'Test structure out of sync.'; \
		if [ -n "$$MISSING_TESTS" ]; then \
			echo ''; \
			echo 'Missing test files:'; \
			echo "$$MISSING_TESTS" | sed 's|\([^/]*\)$$|test_\1|'; \
		fi; \
		if [ -n "$$MISSING_SRC" ]; then \
			echo ''; \
			echo 'Missing source files:'; \
			echo "$$MISSING_SRC"; \
		fi; \
		exit 1; \
	fi

# * -------------------------------- *

lint:
	@uv run python -m ruff check src tests
	@uv run python -m ruff format --check src tests

format:
	@uv run python -m ruff check --fix src tests
	@uv run python -m ruff format src tests

# * -------------------------------- *