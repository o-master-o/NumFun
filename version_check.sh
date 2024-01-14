#!/bin/bash

FOUND_PYTHON_PATH=""

check_python_version() {
    local python_executable=$1
    $python_executable -c "import sys; exit(1) if sys.version_info < (3, 10) else exit(0)"
    return $?
}

check_system_python() {
    if command -v python3 &>/dev/null && check_python_version python3; then
        FOUND_PYTHON_PATH=$(command -v python3)
        return 0
    fi
    return 1
}

check_usr_share_python() {
    if [ -d "/usr/share/python" ]; then
        for python_executable in /usr/share/python/python*; do
            if check_python_version "$python_executable"; then
                FOUND_PYTHON_PATH="$python_executable"
                return 0
            fi
        done
    fi
    return 1
}

check_pyenv_python() {
    if command -v pyenv &>/dev/null; then
        for version in $(pyenv versions --bare); do
            if check_python_version "pyenv exec python$version"; then
                FOUND_PYTHON_PATH=$(pyenv which python$version)
                return 0
            fi
        done
    fi
    return 1
}

prompt_user_for_python() {
    read -p "Enter the path to a Python >= 3.10 executable: " user_python_path
    if [ -n "$user_python_path" ] && check_python_version "$user_python_path"; then
        FOUND_PYTHON_PATH=$(pyenv which python$version)
        return 0
    else
        return 1
    fi
}

find_suitable_python() {
    check_system_python || check_usr_share_python || check_pyenv_python || prompt_user_for_python
    if [ -n "$FOUND_PYTHON_PATH" ]; then
        echo "Found suitable Python at $FOUND_PYTHON_PATH"
        return 0
    else
        echo "No suitable Python version found."
        return 1
    fi
}
