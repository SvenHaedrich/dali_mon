#!/bin/bash
# check formatting, lint and types of the python code, also used by the CI
# stop if the setup fails
set -e
# run from the directory of this script, also when started from elsewhere
cd "$(dirname "$(realpath "$0")")"
[ -f .venv/bin/activate ] || python3 -m venv .venv
source .venv/bin/activate
echo "--- update requirements"
python3 -m pip install --upgrade pip
python3 -m pip install -e ../.. --group ../../pyproject.toml:test --group ../../pyproject.toml:lint
cd ../..
result=0
echo "--- ruff format"
ruff format --check --diff || result=1
echo "--- ruff check"
ruff check || result=1
echo "--- pyright"
pyright || result=1
exit $result
