#!/bin/sh -e
set -x

${PYTHONPATH:-python} -m uv run ruff altlinker --fix
${PYTHONPATH:-python} -m uv run black altlinker
${PYTHONPATH:-python} -m uv run isort altlinker
