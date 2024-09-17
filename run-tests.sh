#!/bin/bash

# Run tests on application.
# Show coverage report if all tests pass.

set -o nounset
set -o errexit
set +o xtrace


# Abort run if Ruff picks up any errors
#ruff check --output-format grouped


# Run unitests, show files without 100% branch coverage
coverage run --branch -m unittest
coverage report --show-missing --skip-covered
coverage erase

# Check optional static typing
#mypy --sqlite-cache .
