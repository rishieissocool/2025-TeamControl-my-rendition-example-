#! /usr/bin/env python3

import os
import subprocess
import sys
import logging
import traceback
import platform
import shutil

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def check_python_version():
    """Check if the Python version is supported."""
    required_version = (3, 9)
    if sys.version_info < required_version:
        sys.exit(f"Python {required_version[0]}.{required_version[1]} or higher is required. "
                 f"You are using Python {sys.version_info.major}.{sys.version_info.minor}.")

def check_venv_exist():
    """Ensure the venv module is available and install it if possible."""
    try:
        import venv
    except ImportError:
        print("[!] Python 'venv' module not found. Attempting to install it...")
        os_name = platform.system()

        try:
            if os_name == "Linux":
                if shutil.which("apt"):
                    subprocess.check_call(["sudo", "apt", "update"])
                    subprocess.check_call(["sudo", "apt", "install", "-y", "python3-venv"])
                elif shutil.which("dnf"):
                    subprocess.check_call(["sudo", "dnf", "install", "-y", "python3-venv"])
                elif shutil.which("yum"):
                    subprocess.check_call(["sudo", "yum", "install", "-y", "python3-venv"])
                else:
                    raise RuntimeError("Unsupported Linux distro — install python3-venv manually.")
            elif os_name == "Darwin":
                if shutil.which("brew"):
                    subprocess.check_call(["brew", "install", "python"])
                else:
                    raise RuntimeError("Install Homebrew and run: brew install python")
            elif os_name == "Windows":
                raise RuntimeError("Please re-run the Python installer and ensure 'venv' is selected.")
            else:
                raise RuntimeError(f"Unsupported OS: {os_name}")
        except Exception as e:
            logging.error(f"Failed to install venv: {e}")
            sys.exit(1)
    print("python venv found")

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

def get_pip_path(venv_dir):
    """Get the pip executable path inside the virtual environment."""
    if os.name == "nt":
        return os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_dir, "bin", "pip")

def create_virtual_env():
    """Create a virtual environment and install dependencies."""
    venv_dir = ".venv"
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        print("Virtual environment created.")
    else:
        print("Virtual environment already exists. Skipping creation.")

    # gets the virtual environment pip path
    pip_path = get_pip_path(venv_dir)
    
    print("Upgrading pip and installing dependencies...")
    try:
        subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
        subprocess.check_call([pip_path, "install", "-U", "setuptools", "wheel"])
        subprocess.check_call([pip_path, "install", "-e", "."])
        print("Dependencies installed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing dependencies: {e}")
        print("Failed to install dependencies. Check logs for more information.")

def run_shell_script(script_name):
    """Run a shell script (works on Linux/macOS, and Git Bash on Windows)."""
    try:
        if not os.path.exists(script_name):
            raise FileNotFoundError(f"{script_name} not found.")
        print(f"Executing {script_name}...")
        subprocess.check_call(["bash", script_name])
    except Exception as e:
        logging.error(f"Failed to run {script_name}: {e}")
        logging.debug(traceback.format_exc())
        print("--- Skipping ---")
        print("If you're on Windows, please run this in Git Bash or WSL.")

def main():
    print("This is an automated script that installs virtual environment base on your system")
    print("If you are using windows, please make sure that you are using the 'git bash' Terminal, or it won't work")
    check_python_version()
    check_venv_exist()

    if prompt_yn("Would you like to install a virtual environment and dependencies?"):
        create_virtual_env()

    if prompt_yn("Would you like to activate the virtual environment and pull the latest changes from the Git repository?"):
        run_shell_script("setup.sh")

    print("✅ Setup complete!")

if __name__ == "__main__":
    main()