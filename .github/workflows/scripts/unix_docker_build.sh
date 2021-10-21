#!/bin/bash

set -ex

# Parse ARGs
for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)
    case "$KEY" in
            CI_SETUP_CMAKE_ARGS)              SHA=${VALUE} ;;
            PY)               PY=${VALUE} ;;
            *)
    esac
done

source /home/dev/miniconda/etc/profile.d/conda.sh
conda activate $PY

cd taichi
python3 -m pip install -r requirements_dev.txt
python3 -m pip install torch==1.9.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
TAICHI_CMAKE_ARGS=$CI_SETUP_CMAKE_ARGS python3 setup.py install 

export TI_IN_DOCKER=true

ti diagnose
ti test -vr2 -t2 -k "not ndarray and not torch"
ti test -vr2 -t1 -k "ndarray or torch"
