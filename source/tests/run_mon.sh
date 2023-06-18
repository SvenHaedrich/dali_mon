#!/bin/bash
set +x
cd ..
echo "--- activate virtual environemnt"
source ../env/bin/activate
echo "--- update requirements"
pip3 install -r tests/requirements.txt
echo "--- execute script"
coverage run -m pytest tests/mon/ $*
coverage report
