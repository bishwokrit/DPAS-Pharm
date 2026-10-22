#!/usr/bin/env bash
# One command to run the pipeline. Examples:  ./run.sh status   ./run.sh L01   ./run.sh all
cd "$(dirname "$0")" && python3 pipeline/run.py "$@"
