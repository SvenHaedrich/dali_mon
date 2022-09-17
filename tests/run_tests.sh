#!/bin/bash
set +x
echo "--- activate virtual environemnt"
source ../env/bin/activate
echo "--- update requirements"
pip3 install -r requirements.txt
echo "--- execute script"
export PYTHONPATH=$(pwd)
python3 -m pytest --version
python3 -m pytest scripts/ $*
