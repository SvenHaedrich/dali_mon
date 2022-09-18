#!/bin/bash
set +x
echo "--- activate virtual environemnt"
source ../env/bin/activate
echo "--- update requirements"
pip3 install -r requirements.txt
echo "--- execute script"
coverage run -m pytest scripts/ $*
coverage report
