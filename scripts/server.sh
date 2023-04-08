#!/bin/bash

set -e

${PYTHONPATH:-python} -m poetry install
${PYTHONPATH:-python} -m uvicorn altlinker.server:app --reload --port ${PORT:-8001}
