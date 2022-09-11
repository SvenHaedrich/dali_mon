#!/bin/bash
set +x
echo "--- activate virtual environemnt"
source ./env/bin/activate
echo "--- update requirements"
pip3 install -r requirements.txt
echo "--- execute script"
python3 source/main.py --version
python3 source/main.py $*