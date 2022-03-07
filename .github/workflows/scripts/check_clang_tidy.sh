#!/bin/bash

CI_SETUP_CMAKE_ARGS=$1

cd test_actions
python3 -m pip install -r requirements_dev.txt

rm -rf build && mkdir build && cd build
cmake $CI_SETUP_CMAKE_ARGS ..

cd ..
python3 ./scripts/run_clang_tidy.py $PWD/test_actions -clang-tidy-binary clang-tidy-10 -checks=-*,performance-inefficient-string-concatenation,readability-identifier-naming -header-filter=$PWD/test_actions -p $PWD/build -j2
