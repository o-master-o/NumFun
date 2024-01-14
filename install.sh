#!/bin/bash
SCRIPT_DIR=$(dirname "$0")
BASHRC="$HOME/.bashrc"
VENV_DIR=$SCRIPT_DIR/venv
VENV_PYTHON_PATH="$VENV_DIR/bin/python"
START_APP_PATH="$SCRIPT_DIR/start.py"
source $SCRIPT_DIR/version_check.sh
START_TAG="# NumFun game -- start tag"
END_TAG="# NumFun game -- end tag"


clear_screen () {
    clear -x
}

add_to_bashrc() {
    echo "$1" >> "$BASHRC"
}

clean_bashrc () {
    if grep -q "$START_TAG" "$BASHRC"; then
        sed -i "/$START_TAG/,/$END_TAG/d" "$BASHRC"
    fi
}

remove_venv () {
    rm -rf "$SCRIPT_DIR/venv"
}

install_virtualenv_if_needed() {
    if ! command -v virtualenv &> /dev/null; then
        echo "virtualenv is not installed. Installing it now..."
        sudo apt-get update
        sudo apt-get install -y virtualenv
        echo "virtualenv has been installed."
    else
        echo "virtualenv is already installed."
    fi
}


clean_environment () {
    clean_bashrc
    remove_venv
}


create_virtualenv() {
    local python_executable=$1
    virtualenv -p $python_executable "$VENV_DIR"
    echo "Virtual environment created in $VENV_DIR"
}


install_requirements() {
    pip install -r "$SCRIPT_DIR/requirements/base.txt"
}

add_shebang_to_start_file() {
    $VENV_PYTHON_PATH
}

replace_or_add_shebang() {
    local file_path="$1"
    local new_shebang="$2"

    if [[ $(head -n 1 "$file_path") == \#!* ]]; then
        sed -i "1s|^.*$|$new_shebang|" "$file_path"
    else
        sed -i "1i$new_shebang" "$file_path"
    fi
}


# Installation steps ---------->

if ! find_suitable_python; then
    echo "Installation cannot proceed without a suitable Python version."
    exit 1
fi

clear_screen
echo "Using Python at $FOUND_PYTHON_PATH for installation."
clean_environment
install_virtualenv_if_needed
create_virtualenv $FOUND_PYTHON_PATH
replace_or_add_shebang "$START_APP_PATH" "#!$VENV_PYTHON_PATH"
add_to_bashrc "$START_TAG"

source "$VENV_DIR/bin/activate"
install_requirements
"$VENV_PYTHON_PATH" "$START_APP_PATH" --install-completion
deactivate

add_to_bashrc "$END_TAG"
clear_screen

$START_APP_PATH
