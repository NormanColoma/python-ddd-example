#!/bin/sh
set -e

poetry config virtualenvs.in-project true

if [ ! -d ".venv" ]; then
  echo "Virtual environment not found. Installing dependencies..."
  poetry install
else
  echo "Virtual environment found. Skipping poetry install."
fi

exec "$@"
