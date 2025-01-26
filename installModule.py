#! /usr/bin/env python3

## Python script to activate module and virtual env
import os
import subprocess
import sys
import logging
import traceback

# Set up logging configuration
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def check_python_version():
    """Check if the Python version is supported."""
    required_version = (3, 9)  # Minimum required Python version
    if sys.version_info < required_version:
        sys.exit(f"Python {required_version[0]}.{required_version[1]} or higher is required. You are using Python {sys.version_info.major}.{sys.version_info.minor}.")

def prompt_yn(question):
    """Prompt the user with a Y/N question."""
    while True:
        answer = input(f"{question} (Y/N): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        elif answer in {"n", "no"}:
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

def create_virtual_env():
    """Create a virtual environment and install dependencies."""
    venv_dir = ".venv"
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        print("Virtual environment created.")
    else:
        print("Virtual environment already exists. Skipping creation.")
    
    print("Upgrading pip and installing dependencies...")
    try:
        pip_path = get_pip_path(venv_dir)
        subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
        subprocess.check_call([pip_path, "install", "-U", "setuptools", "wheel"])
        subprocess.check_call([pip_path, "install", "-e", "."])
    except subprocess.CalledProcessError as e:
        print(f"error when installing dependencies. {e}")

def get_pip_path(venv_dir):
    """ Gets the pip Local Path"""
    if os.name == "nt": #windows
        return os.path.join(venv_dir, "Scripts", "pip.exe")
    else: #Linux / Mac
        return os.path.join(venv_dir, "bin", "pip")
    
def run_shell_script(script_name):
    """Run a shell script."""
    try:
        print(f"Executing {script_name} . . .")
        subprocess.check_call(["bash", script_name])

    except Exception as e:
        error_type = type(e).__name__
        logging.error(f"{script_name} cannot be executed. TYPE : {error_type}, Please use a git bash Terminal IF YOU ARE ON WINDOWS")
        logging.debug(f"TRACEBACK {error_type}",exc_info=True)
        print("--- Skipping ---")
        return

def main():
    check_python_version()

    # Ask user whether to install the virtual environment
    if prompt_yn("Would you like to install a virtual environment and dependencies?"):
        create_virtual_env()

    # Trigger the shell script to handle the virtual environment activation and git pull
    if prompt_yn("Would you like to activate the virtual environment and pull the latest changes from the Git repository?"):
        run_shell_script("setup.sh")

    print("Setup complete!")

if __name__ == "__main__":
    main()
