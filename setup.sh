#linux
# ! /usr/bin/bash 

# Check if virtual environment exists
VENV_DIR=".venv"
if [ -d "$VENV_DIR" ]; then
   # Check OS and use the correct activate script path
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        # For Linux and macOS
        source "$VENV_DIR/bin/activate"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # For Git Bash on Windows
        source "$VENV_DIR/Scripts/activate"
    else
        echo "Unsupported OS. Could not activate the virtual environment."
        exit 1
    fi

    # Notify user that the environment is activated
    echo "Virtual environment activated successfully!"

    # Provide user instructions to activate it manually if needed
    echo -e "\nTo activate the virtual environment manually, run:"
    echo "    source $VENV_DIR/bin/activate  # for Linux/macOS"
    echo "    source $VENV_DIR/Scripts/activate  # for Git Bash on Windows"

fi



echo " - - - Installing Python Module - - - "

pip3 install --editable . # add "--user" to this if you don't have access to your computer's system-wide python packages.

echo " - - - Performing Git Pull - - - "
git pull || { echo "Git pull failed"; exit 1; }


