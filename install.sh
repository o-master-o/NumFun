#!/bin/bash
SCRIPT_DIR=$(dirname "$0")
VENV_DIR=$SCRIPT_DIR/venv
source $SCRIPT_DIR/version_check.sh
START_TAG="# NumFun game -- start tag"
END_TAG="# NumFun game -- end tag"
BASHRC="$HOME/.bashrc"

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
    source "$VENV_DIR/bin/activate"
    pip install -r "$SCRIPT_DIR/requirements/base.txt"
    deactivate
}

show_welcome_header () {
    echo -e "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
    echo -e "┃                                                                   ┃"
    echo -e "┃   ███╗   ██╗██╗   ██╗███╗   ███╗    ███████╗██╗   ██╗███╗   ██╗   ┃"
    echo -e "┃   ████╗  ██║██║   ██║████╗ ████║    ██╔════╝██║   ██║████╗  ██║   ┃"
    echo -e "┃   ██╔██╗ ██║██║   ██║██╔████╔██║    █████╗  ██║   ██║██╔██╗ ██║   ┃"
    echo -e "┃   ██║╚██╗██║██║   ██║██║╚██╔╝██║    ██╔══╝  ██║   ██║██║╚██╗██║   ┃"
    echo -e "┃   ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║    ██║     ╚██████╔╝██║ ╚████║   ┃"
    echo -e "┃   ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝   ┃"
    echo -e "┃                                                                   ┃"
    echo -e "┃   ═══════════ Welcome to NumFun! Let's Enjoy Math! ════════════   ┃"
    echo -e "┃                                                                   ┃"
    echo -e "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
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
install_requirements
add_to_bashrc "$START_TAG"


add_to_bashrc "$END_TAG"
clear_screen
show_welcome_header
