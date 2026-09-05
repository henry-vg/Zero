SHELL := /bin/bash

.PHONY:
	run \
	test \
	test-with-coverage \
	test-with-coverage-and-reports \
	test-structure \
	compile-requirements \
	check-requirements

# * -------------------------------- *

run:
	@python -m src.host.main

# * -------------------------------- *

test:
	@python -m pytest tests

test-with-coverage:
	@python -m pytest tests --cov=src && \
	rm .coverage

test-with-coverage-and-reports:
	@python -m pytest tests --cov=src --cov-report=term-missing --cov-report=xml && \
	rm .coverage

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
	fi

# * -------------------------------- *

REQUIREMENTS_TXT_PATH = "requirements.txt"
REQUIREMENTS_IN_PATH = "requirements.in"

compile-requirements:
	@if CUSTOM_COMPILE_COMMAND='make compile-requirements' python -m piptools compile --resolver=backtracking --strip-extras --output-file=$(REQUIREMENTS_TXT_PATH) $(REQUIREMENTS_IN_PATH) >/dev/null 2>&1; then \
			echo 'Requirements compiled successfully.'; \
		else \
			echo 'Failed to compile requirements.'; \
		fi

check-requirements:
	@tmp_file="$$(mktemp)"; \
	trap 'rm -f "$$tmp_file"' EXIT; \
	cp $(REQUIREMENTS_TXT_PATH) "$$tmp_file"; \
	CUSTOM_COMPILE_COMMAND='make compile-requirements' python -m piptools compile --resolver=backtracking --strip-extras --quiet --output-file="$$tmp_file" $(REQUIREMENTS_IN_PATH) >/dev/null; \
	if ! diff -q $(REQUIREMENTS_TXT_PATH) "$$tmp_file" >/dev/null; then \
		echo 'Requirements out of sync. Try running "make compile-requirements".'; \
	else \
		echo 'Requirements up to date.'; \
	fi
	
# * -------------------------------- *