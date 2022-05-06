# Build script for windows

$ErrorActionPreference = "Stop"

$RepoURL = 'https://github.com/taichi-dev/taichi'
clang --version

WriteInfo("Setting up Python environment")
