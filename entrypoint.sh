#!/bin/bash
set -e

# Dependencies are installed at image build time (see Dockerfile).  If you
# change pyproject.toml or setup.py, rebuild the image with:
#
#     docker compose build
#
# That keeps container startup instant in the common case of editing .py files.

if [ $# -eq 0 ]; then
    exec bash
else
    exec "$@"
fi