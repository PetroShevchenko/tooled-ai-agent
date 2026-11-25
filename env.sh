#!/usr/bin/env bash

export LITELLM_LOCAL_MODEL_COST_MAP="True"

usage() {
    echo "${DARK_GREEN}Use: ${GREEN}source ./env.sh [activate|deactivate]${RESET}"
}

# This file should be included to the current Bash-terminal through source.
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    usage
    exit 1
fi

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ACTION="${1:-activate}"
source "$PROJECT_DIR/colors.sh"

case "$ACTION" in
    activate)
        if [[ ! -f "$PROJECT_DIR/.venv/bin/activate" ]]; then
            echo "${RED}Environment .venv not found. First execute: ./install.sh${RESET}"
            return 1
        fi
        source "$PROJECT_DIR/.venv/bin/activate"
        echo "${GREEN}Virtual environment activated${RESET}"
        ;;
    deactivate)
        if declare -F deactivate >/dev/null; then
            deactivate
            echo "${GREEN}Virtual environment deactivated${RESET}"
        else
            echo "${YELLOW}Virtual environment is not activated now${RESET}"
        fi
        ;;
    *)
        usage
        return 2
        ;;
esac