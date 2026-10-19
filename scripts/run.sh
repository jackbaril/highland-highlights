#!/bin/bash

# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

readonly ENTRY_POINT="highland-highlights/main.py"
readonly PROJECT_DIR_NAME="highland-highlights"
readonly SCRIPT_NAME="${0##*/}"
readonly SCRIPT_DIR="$(dirname "$0")"
readonly VENV_DIR=".venv"

err() {
  echo "${SCRIPT_NAME}: $*" >&2
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

check_venv() {
  if [[ ! -f "${VENV_DIR}/bin/python3" ]]; then
    err "${VENV_DIR}: virtual environment not found"
    echo "run '${SCRIPT_DIR}/setup.sh' to initialize environment" >&2
    exit 1
  fi
}

main() {
  cd_project_root
  check_venv

  exec "${VENV_DIR}/bin/python3" "${ENTRY_POINT}" "$@"
}

main "$@"
