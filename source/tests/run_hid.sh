#!/bin/bash
set +x
cd ..
[ -f venv/bin/activate ] || python3 -m venv venv
echo "--- activate virtual environemnt"
source ../venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r tests/requirements.txt
echo "--- execute script"
coverage run -m pytest tests/hid/ $*
coverage report
