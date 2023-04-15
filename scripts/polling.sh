#!/bin/bash

set -e

${PYTHONPATH:-python} -m altlinker.telegram_handler
