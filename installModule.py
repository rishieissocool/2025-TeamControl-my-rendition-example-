## Python script to activate module and virtual env
import os
import subprocess
import sys

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
    subprocess.check_call([os.path.join(venv_dir, "bin", "pip"), "install", "--upgrade", "pip"])
    subprocess.check_call([os.path.join(venv_dir, "bin", "pip"), "install", "-U", "setuptools", "wheel"])
    subprocess.check_call([os.path.join(venv_dir, "bin", "pip"), "install", "-e", "."])

def run_shell_script(script_name):
    """Run a shell script."""
    try:
        subprocess.check_call([script_name], shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_name}: {e}")
        sys.exit(1)

def main():
    check_python_version()

    # Ask user whether to install the virtual environment
    if prompt_yn("Would you like to install a virtual environment and dependencies?"):
        create_virtual_env()

    # Trigger the shell script to handle the virtual environment activation and git pull
    if prompt_yn("Would you like to activate the virtual environment and pull the latest changes from the Git repository?"):
        run_shell_script("./setup.sh")

    print("Setup complete!")

if __name__ == "__main__":
    main()
