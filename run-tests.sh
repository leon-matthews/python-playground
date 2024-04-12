#!/bin/bash

# Run tests on application.
# Show coverage report if all tests pass.

set -o nounset
set -o errexit
set +o xtrace

python3 -m unittest
