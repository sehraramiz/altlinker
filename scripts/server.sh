#!/bin/bash

set -e

${PYTHONPATH:-python} -m pip install uv
${PYTHONPATH:-python} -m uv sync
${PYTHONPATH:-python} -m uv run uvicorn altlinker.server:app --reload --port ${PORT:-8001}
