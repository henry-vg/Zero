.PHONY:
	run \
	test \
	test-with-coverage \
	test-with-coverage-and-reports \
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

# * -------------------------------- *

REQUIREMENTS_TXT_PATH = "requirements.txt"
REQUIREMENTS_IN_PATH = "requirements.in"

compile-requirements:
	@if CUSTOM_COMPILE_COMMAND='make compile-requirements' python -m piptools compile --resolver=backtracking --strip-extras --output-file=$(REQUIREMENTS_TXT_PATH) $(REQUIREMENTS_IN_PATH) >/dev/null 2>&1; then \
			echo 'Compiled successfully.'; \
		else \
			echo 'Failed to compile.'; \
		fi

check-requirements:
	@tmp_file="$$(mktemp)"; \
	trap 'rm -f "$$tmp_file"' EXIT; \
	cp $(REQUIREMENTS_TXT_PATH) "$$tmp_file"; \
	CUSTOM_COMPILE_COMMAND='make compile-requirements' python -m piptools compile --resolver=backtracking --strip-extras --quiet --output-file="$$tmp_file" $(REQUIREMENTS_IN_PATH) >/dev/null; \
	if ! diff -q $(REQUIREMENTS_TXT_PATH) "$$tmp_file" >/dev/null; then \
		echo 'Out of sync. Try running "make compile-requirements".'; \
	else \
		echo 'Up to date.'; \
	fi
	
# * -------------------------------- *