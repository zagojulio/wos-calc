#!/bin/bash

# Set Python path to include project root
export PYTHONPATH=.

# Run tests with coverage
pytest --verbose \
    --cov=features \
    --cov=utils \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-fail-under=80 