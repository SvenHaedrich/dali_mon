#!/bin/bash
# stop if the setup fails
set -e
# run from the directory of this script, also when started from elsewhere
cd "$(dirname "$(realpath "$0")")"
[ -f .venv/bin/activate ] || python3 -m venv .venv
echo "--- activate virtual environment"
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e ../.. --group ../../pyproject.toml:test
echo "--- execute script"
cd ..
# the result of the tests, not of the coverage report, is the exit code
result=0
coverage run -m pytest tests/hid/ "$@" || result=$?
coverage report
exit $result
