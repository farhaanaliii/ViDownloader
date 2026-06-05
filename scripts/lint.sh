#!/usr/bin/env bash
set -e

echo "Running isort..."
isort .

echo "Running black..."
black .

echo "Running flake8..."
flake8 .

echo "Done!"
