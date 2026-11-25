#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"
source ./colors.sh

PYTHON="${PYTHON:-python3}"

"$PYTHON" -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev,docs]"
echo "${GREEN}Installed. ${DARK_GREEN}Please activate environment as follows: ${GREEN}source ./env.sh activate${RESET}"