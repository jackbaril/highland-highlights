#!/bin/bash

readonly ENV_FILE=".env"
readonly PROJECT_DIR_NAME="highland-highlights"
readonly REQUIREMENTS_FILE="requirements.txt"
readonly SCRIPT_NAME="${0##*/}"
readonly VENV_DIR=".venv"

err() {
  echo "${SCRIPT_NAME}: $*" >&2
}

check_dependencies() {
  local cmd
  for cmd in curl python3; do
    if ! command -v "${cmd}" >/dev/null 2>&1; then
      err "'${cmd}': command not found"
      exit 1
    fi
  done

  local python_version
  python_version="$(
    python3 -c '
import sys

print(f"{sys.version_info.major}.{sys.version_info.minor}")
'
  )"

  if ! python3 -c '
import sys

sys.exit(sys.version_info < (3, 10))
  '; then
    err "python3: requires version 3.10 or later; found ${python_version}"
    exit 1
  fi

  if ! python3 -c "import venv" >/dev/null 2>&1; then
    err "python3: 'venv' module not found"
    exit 1
  fi
}

cd_project_root() {
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

  if [[ "${script_dir##*/}" == "scripts" ]]; then
    cd "${script_dir}/.." || exit 1
  else
    cd "${script_dir}" || exit 1
  fi

  if [[ "${PWD##*/}" != "${PROJECT_DIR_NAME}" ]]; then
    err "cannot access project root '${PROJECT_DIR_NAME}'"
    exit 1
  fi
}

validate_api_key() {
  local api_key="$1"

  if [[ -z "${api_key}" ]]; then
    err "API key is required"
    return 1
  fi

  local response
  if ! response="$(
    curl -fsS \
      "https://api.weatherapi.com/v1/current.json?key=${api_key}&q=gilbert" \
      2>&1
  )"; then
    err "weatherapi.com: ${response}"
    return 1
  fi

  local api_error
  api_error="$(
    python3 -c '
import json
import sys

try:
    response = json.load(sys.stdin)
    print(response.get("error", {}).get("message", ""))
except json.JSONDecodeError:
    print("invalid response")
' <<< "${response}"
  )"

  if [[ -n "${api_error}" ]]; then
    err "weatherapi.com: ${api_error}"
    return 1
  fi

  return 0
}

configure_api_key() {
  local api_key=""

  while true; do
    echo -n 'Please enter your API key from weatherapi.com: '
    read api_key
    if validate_api_key "${api_key}"; then
      echo "WEATHER_API_KEY=${api_key}" > "${ENV_FILE}"
      break
    fi
  done
}

setup_venv() {
  if ! python3 -m venv "${VENV_DIR}"; then
    err "failed to create virtual environment '${VENV_DIR}'"
    exit 1
  fi

  if ! "${VENV_DIR}/bin/python3" -m pip install -r "${REQUIREMENTS_FILE}"; then
    err "failed to install dependencies from ${REQUIREMENTS_FILE}"
    exit 1
  fi
}

main() {
  check_dependencies
  cd_project_root
  mkdir -p assets/documents
  configure_api_key
  setup_venv

  echo "Setup completed successfully."
  echo "Please return to the README for further instructions."
}

main "$@"
