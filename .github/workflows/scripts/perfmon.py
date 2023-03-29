#!/usr/bin/env python3 -u

import os
from pathlib import Path

if os.environ.get('IN_DOCKER'):
    os.chdir(Path('taichi').resolve())

#. $(dirname $0)/common-utils.sh

#[[ "$IN_DOCKER" == "true" ]] && cd tiiaichi

#python3 .github/workflows/scripts/build.py --write-env=/tmp/ti-env.sh
#. /tmp/ti-env.sh

## TODO: hard code Android NDK path in Docker image, should be handled by build.py
#export ANDROID_NDK_ROOT=/android-sdk/ndk-bundle

#python -m pip install dist/*.whl

#TAG=$(git describe --exact-match --tags 2>/dev/null || true)
#if [ ! -z "$TAG" ]; then
#    MORE_TAGS="--tags type=release,release=$TAG"
#else
#    MORE_TAGS=""
#fi

#git clone https://github.com/taichi-dev/taichi_benchmark
#cd taichi_benchmark
#pip install -r requirements.txt
#python run.py --upload-auth $BENCHMARK_UPLOAD_TOKEN $MORE_TAGS
