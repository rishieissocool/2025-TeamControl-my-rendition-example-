## This installs the game controller and it only runs on ubuntu linux at the moment.

echo "Installing gameController please do not touch until you see the phrase - 'END'";

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then

        echo " *** updating destination to /home/ssl.*** "
        cd 
        ## Verifying default home
        if [ -z "$HOME" ]; then
            echo "HOME variable is not set. Exiting."
            exit 1
        fi

        SSL_DIR="$HOME/ssl"
        
        if [ ! -d "$SSL_DIR" ]; then
            echo "Directory : $SSL_DIR not found. Creating directory . . ."
            mkdir -p "$SSL_DIR" || { echo "Fail to create Directory $SSL_DIR"; exit 1; }
        fi

        cd "$SSL_DIR" || { echo "Failed to cd into $SSL_DIR"; exit 1;}
       

        echo "*** Updating System ***"
        sudo apt update
        sudo apt upgrade -y

        echo "*** Installing Software Dependency ***"

        ## The game controller requires a node JS version above 20, so we will be using the following script.
        echo "- Installing NodeJS version 20"
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
        source ~/.bashrc
        nvm install v22.14.0
        nvm list
        echo "NodeJS has now been installed with Version:"
        node -v

        echo "- Installing GO"
        sudo apt install golang-go -y
        go version

        echo "- Installing Java SDK for Tiger's AutoRef"
        sudo apt install openjdk-21-jdk -y

        echo "*** Cloning Git Repository -> SSL - Game Controller ***"
        git clone https://github.com/RoboCup-SSL/ssl-game-controller.git

        ## Activate make install
        sudo make install


        if [ ! -d "$SSL_DIR/TOGERS" ]; then ## IF the folder TIGERS that is used to store Tigers' AutoRef does not exist
            mkdir TIGERS
            cd TIGERS
            echo "*** Cloning Git Repository -> TIGERs's Autoref***"
            git clone https://github.com/TIGERs-Mannheim/AutoReferee.git 
                       
        else           
            echo "TIGER's AutoRef Already Cloned"
            cd TIGERS
        fi
        ./build.sh
    fi

