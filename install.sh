#linux
# ! /usr/bin/bash 
# replace above line with '! /usr/bin/env bash' if you are planning to use virutal env

#UNCOMMENT if you run into a permission error when installing this module on ubuntu.

read -p"Do you want Virtual Environment [y/n] : " ans
case $ans in 
    y) echo "Begin installation in Virtual Environment";
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    
            if ! command -v virtualenv &> /dev/null; then
                sudo apt install virtualenv
            fi 
            virtualenv . ;
            source ./bin/activate;
        
        # elif [[ "$OSTYPE" == "msys"* ]]; then 
        #     pip3 install virtualenv
        #     pip3 install virtualenvwrapper-win
        #     mkvirtualenv .
        else
            echo "Sorry virtual env only supported in Linux";

        fi
        

esac

# Installing Python Module 
pip3 install --editable . # add "--user" to this if you don't have access to your computer's system-wide python packages.

# Initiallisng Submodules
git submodule update --init 
# Modifying configs to allow recursive pulling submodule
git config submodule.recurse true 
# Initiate git pull
git pull


