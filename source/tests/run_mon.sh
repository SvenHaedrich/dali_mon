#!/bin/bash
set +x
[ -f venv/bin/activate ] || python3 -m venv .venv
source .venv/bin/activate
echo "--- update requirements"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "--- execute script"
cd ..
coverage run -m pytest tests/mon/ $*
coverage report
