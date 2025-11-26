#! /bin/bash

### THIS SCRIPT REQUIRES (GIT) BASH TERMINAL ###

# Check if virtual environment exists
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; 
then
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Add Deadsnakes repo
        sudo apt update
        sudo apt install -y software-properties-common
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt update
        sudo apt-get install -y \
            python3.13 python3.13-venv python3.13-dev python3.13-tk

    fi 
    python3.13 -m venv "$VENV_DIR" || { echo "cannot initiate virtual environment."; exit 1; }

fi
if [ -d "$VENV_DIR" ]; then
   # Check OS and use the correct activate script path
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        # linux and macOS
        source "$VENV_DIR/bin/activate"

        
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # For Git Bash on Windows
        source "$VENV_DIR/Scripts/activate"

    else
        echo "Unsupported OS. Could not activate the virtual environment."
        exit 1
    fi
fi
# exec "$SHELL" -l 


# Notify user that the environment is activated
echo "Virtual environment activated successfully!"

# Provide user instructions to activate it manually if needed
echo "*** There is a chance that your environment did not activate automatically ***"
echo -e "\nTo activate the virtual environment manually, run:"
echo "    source $VENV_DIR/bin/activate  # for Linux/macOS"
echo "    source $VENV_DIR/Scripts/activate  # for Git Bash on Windows"




echo -e "\n - - - Installing Python Module - - - "

pip install --editable . # add "--user" to this if you don't have access to your computer's system-wide python packages.
# pip3 install -e .[trajectory]
# pip3 install -e .[pathplanning]
echo -e "\n - - - Performing Git Pull - - - "
git pull || { echo "Git pull failed"; exit 1; }


