#!/bin/sh -e
set -x

ruff altlinker --fix
black altlinker
isort altlinker
