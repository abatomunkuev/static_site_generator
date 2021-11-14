#!/bin/bash
echo
echo "Running Python Unit-testing & Code Formatting"
echo
# Use black for formatting
black .
# Use Flake8 for linting tests
flake8 .
# Run Unit-tests
pytest tests/