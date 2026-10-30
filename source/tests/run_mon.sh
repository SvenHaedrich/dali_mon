#!/bin/bash
set +x
# run from the directory of this script, also when started from elsewhere
cd "$(dirname "$(realpath "$0")")"
[ -f .venv/bin/activate ] || python3 -m venv .venv
source .venv/bin/activate
echo "--- update requirements"
python3 -m pip install --upgrade pip
python3 -m pip install -e ../.. --group ../../pyproject.toml:test
echo "--- execute script"
cd ..
coverage run -m pytest tests/mon/ "$@"
coverage report
