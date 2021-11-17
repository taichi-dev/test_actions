#!/bin/bash
set -ex

python3 -m pip uninstall taichi taichi-nightly -y
python3 -m pip install -r requirements_dev.txt
python3 -m pip install -r requirements_test.txt
git fetch origin master
python3 setup.py bdist_wheel

export NUM_WHL=`ls dist/*.whl | wc -l`
if [ $NUM_WHL -ne 1 ]; then echo `ERROR: created more than 1 whl.` && exit 1; fi
python3 -m pip install dist/*.whl
