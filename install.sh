#!/bin/bash
SCRIPT_DIR=$(realpath $(dirname "$0"))
BASHRC="$HOME/.bashrc"
VENV_DIR=$SCRIPT_DIR/venv
VENV_PYTHON_PATH="$VENV_DIR/bin/python"
START_APP_PATH="$SCRIPT_DIR/num_fun/start.py"
TMP_DIR="$HOME/.config/NumFun/tmp"
START_APP_LINK="$TMP_DIR/numfun"
source $SCRIPT_DIR/version_check.sh
START_TAG="# NumFun game -- start tag"
END_TAG="# NumFun game -- end tag"

# Colors
BLUE="\033[34;1m"
YELLOW="\033[93;1m"
NC="\033[0m"

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

remove_tmp() {
    rm -rf $TMP_DIR
}

clean_environment () {
    clean_bashrc
    remove_venv
    remove_tmp
}

get_python_version () {
    local RAW_PYTHON_VERSION=$($1 --version)
    USED_PYTHON_VERSION=${RAW_PYTHON_VERSION#* }
    USED_PYTHON_SHORT_VERSION=${USED_PYTHON_VERSION%.*}
}

install_if_not_installed() {
    package=$1

    if ! dpkg -s "$package" &> /dev/null; then
        echo "Package $package is not installed. Installing..."
        sudo apt-get update
        sudo apt-get install -y "$package"
    else
        echo "Package $package is already installed."
    fi
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

# # Installation steps ---------->
clear_screen
if ! find_suitable_python; then
    echo "Installation cannot proceed without a suitable Python version."
    exit 1
fi
echo "Using Python at $FOUND_PYTHON_PATH for installation."
get_python_version $FOUND_PYTHON_PATH
clean_environment
install_if_not_installed virtualenv
install_if_not_installed "libpython$USED_PYTHON_SHORT_VERSION-dev"
create_virtualenv $FOUND_PYTHON_PATH

add_to_bashrc "$START_TAG"
add_to_bashrc "export PYTHONPATH='/home/yoda/work/python_projects/NumFun:$PYTHONPATH'"
add_to_bashrc "alias num-fun='$VENV_PYTHON_PATH $START_APP_PATH'"
source "$VENV_DIR/bin/activate"
install_requirements
"$VENV_PYTHON_PATH" "$START_APP_PATH" --install-completion
deactivate
add_to_bashrc "$END_TAG"
alias num-fun='$VENV_PYTHON_PATH $START_APP_PATH'
clear_screen
echo -e "${BLUE}Installation complete${NC}"
echo -e "Type ${YELLOW}num-fun${NC} to start the game"
