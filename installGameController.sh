#!/bin/bash
## This installs the game controller and it only runs on ubuntu linux at the moment.

## Function to compare versions 
version_lt() {
  [ "$1" = "$2" ] && return 1
  dpkg --compare-versions "$1" lt "$2"
}

echo "Installing gameController please do not touch until you see the phrase - 'END'";
    NODEJS_VERSION="22.14.0"
    GO_VERSION="1.24.1"
    SSL_DIR="$HOME/ssl-software"
    GC_DIR="ssl-game-controller"
    SB_DIR="ssl-status-board"
    TIGERS_DIR="TIGERS"
    ERFORCE_DIR="ERFORCE"


    if [[ "$OSTYPE" == "linux-gnu"* ]]; then

        echo " *** updating destination to $SSL_DIR. *** "
        cd 
        ## Verifying default home
        if [ -z "$HOME" ]; then
            echo "HOME variable is not set. Exiting."
            exit 1
        fi

        
        if [ ! -d "$SSL_DIR" ]; then
            echo "Directory : $SSL_DIR not found. Creating directory . . ."
            mkdir -p "$SSL_DIR" || { echo "Fail to create Directory $SSL_DIR"; exit 1; }
        fi

        cd "$SSL_DIR" || { echo "Failed to cd into $SSL_DIR"; exit 1;}
       

        echo "*** Updating System ***"
        ## SELECT YOUR OWN UPGRADE
        sudo apt update
        # sudo apt upgrade -y
        # sudo apt-get dist-upgrade
        sudo apt get full-upgrade

        echo "*** Installing Software Dependency ***"

        ## The game controller requires a node JS version above 20, so we will be using the following script.
        # Ensure nvm is installed
        if ! command -v nvm &>/dev/null; then
            echo "nvm is not installed. Installing now..."
            curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
            export NVM_DIR="$HOME/.nvm"
            source "$NVM_DIR/nvm.sh"
        else
            source "$HOME/.nvm/nvm.sh"
        fi
        if command -v node &>/dev/null; then
            CURRENT_NODEJS=$(node -v | sed 's/v//')
            echo "Installed Node.js version: $CURRENT_NODEJS"
        else
            CURRENT_NODEJS="none"
            echo "Node.js is not installed."
        fi
        
        

        # Check if update is needed
        if [ "$CURRENT_NODEJS" = "none" ] || version_lt "$CURRENT_NODEJS" "$NODEJS_VERSION"; then
            echo "Installing/updating Node.js to latest LTS version..."
            nvm install --lts
            nvm use --lts
            # Verify installation
            node -v
        else
            echo "Node.js is up to date. No update needed."
        fi

        # echo "- Installing NodeJS version 20"
        # curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh 
        # echo "Reloading Terminal"
        # source ~/.bashrc
        # nvm install v22.14.0
        # nvm list
        # echo "NodeJS has now been installed with Version:"
        # node -v

        echo "- Installing GO"
        # sudo apt install golang-go -y
        # go version

        # Get Current (Installed) Go version
        if command -v go &>/dev/null; then
            CURRENT_GO=$(go version | awk '{print $3}' | sed 's/go//')
            echo "Installed Go version: $CURRENT_GO"
        else
            CURRENT_GO="none"
            echo "Go is not installed."
        fi

        # Check if update is needed
        # If the Current Go Version is NONE or Lower that required Go Version
        if [ "$CURRENT_GO" = "none" ] || version_lt "$CURRENT_GO" "$GO_VERSION"; then
            ## Gets the NEW Latest GO version
            echo "Updating Go to the latest GO version..."

            # Remove old versions if necessary
            sudo rm -rf /usr/local/go

            # Download and install the latest GO version
            wget https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
            sudo tar -C /usr/local -xzf go${GO_VERSION}.linux-arm64.tar.gz
            rm go${GO_VERSION}.linux-arm64.tar.gz

            # Add Go to PATH
            export PATH=$PATH:/usr/local/go/bin
            echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
            echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.zshrc

            echo "Go has been updated to version $(go version)"
        else
            echo "Go is up to date. No update needed."
        fi

    
         if [ ! -d "$SSL_DIR/$GC_DIR" ]; then ## IF the game controller folder does not exist
            echo "*** Cloning Git Repository -> SSL - Game Controller ***"
            git clone https://github.com/RoboCup-SSL/ssl-game-controller.git
        else
            echo "Game Controller already Exist"
        fi
        cd $GC_DIR
        ## Activate make install
        sudo make install
        cd $SSL_DIR

        echo "** Installing SSL-Status-Board**"
        echo "Locating folder - $SSL_DIR/$SB_DIR "
        if [ ! -d "$SSL_DIR/$SB_DIR" ]; then ## IF the folder ssl-status-board does not exist
            git clone https://github.com/RoboCup-SSL/ssl-status-board.git
        else
            echo "Status Board already Cloned from GitHub" 
        fi
        cd $SB_DIR
        make install
        cd $SSL_DIR


        echo "** Installing Java SDK for Tiger's AutoRef **"
        sudo apt install openjdk-21-jdk -y

        echo "Locating folder - $SSL_DIR/$TIGERS_DIR "
        if [ ! -d "$SSL_DIR/$TIGERS_DIR"]|| [! -d "$SSL_DIR/$TIGERS_DIR/AutoReferee" ]; then ## IF the folder TIGERS does not exist
            mkdir $TIGERS_DIR
            cd $TIGERS_DIR
            echo "*** Cloning Git Repository -> TIGERs's Autoref***"
            git clone https://github.com/TIGERs-Mannheim/AutoReferee.git 
                       
        else           
            echo "TIGER's Autorefree Already Cloned"
            cd $TIGERS_DIR
        fi
        cd AutoReferee # going into Tiger's AutoREferee Folder
        ./build.sh
        cd ../..

        echo " - Installing ERFORCE - AUTOREF"
        echo "Locating folder - $SSL_DIR/$ERFORCE_DIR "
        if [ ! -d "$SSL_DIR/$ERFORCE_DIR"] || [! -d "$SSL_DIR/$ERFORCE_DIR/autoref" ]; then ## IF the folder ERFORCE does not exist
            mkdir $ERFORCE_DIR 
            cd $ERFORCE_DIR 
            git clone https://github.com/robotics-erlangen/autoref.git 
        else
            echo "$ERFORCE_DIR exists."
        fi

        cd $ERFORCE_DIR/autoref
        ## initialising Submodule
        echo "Initialising ERFORCE GitHub Submodule"
        git submodule update --init
        ## Setting auto pull submodule
        git config submodule.recurse true
        ## Pulling Submodule
        git pull
        echo "Installing Dependencies"
        ./install_ubuntu_deps.sh 
        echo "Building ERFORCE AutoRef package"
        ./buiild.sh

        echo "-- Installation Completed , Returning to : $SSL_DIR"
        cd $SSL_DIR

        echo "*** - E N D - ***"

    fi

