#!/bin/bash
set +x
[ -f .venv/bin/activate ] || python3 -m venv .venv
echo "--- activate virtual environemnt"
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e ../.. --group ../../pyproject.toml:test
echo "--- execute script"
cd ..
coverage run -m pytest tests/hid/ $*
coverage report
