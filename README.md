# Team Control (2025)

This is the Repository for Our server-side operation

To see the difference between this and last year's version, please see [here](/docs/DifferenceFromLastVersion.md). 

---

## Installation 

To install this module, do

```
git clone https://github.com/WSU-TurtleRabbit/2025-teamcontrol.git
```
Run the Python FILE : installModule.py

IF you have encountered Permission Issues, do the following 
(this should only happen to Linux or Mac Users)

```shell
chmod 755 installModule.py
chmod 755 setup.sh
python3 ./installModule.py
```

There are 2 options that you have to answer [Y/N] to:
1. Installing virtual environment
2. Activating Virtual Environment and Performing a GIT PULL

If you have experienced an error at the second option, and you are using a windows, please manually open up a GIT BASH Terminal. 

You might also experience an error with GIT if you have not logged in on VSCODE. Please seek help accordingly.


### Install GRSIM
To install GRSIM on your Linux Device, this repository also has a file to do it automatically for you. 

Please put the following in your Linux Terminal
```shell
chmod 755 installGRSIM.sh
sudo ./installGRSIM.sh
```
This will install grSim at your Home directory in the folder "ssl-software"

### Installing Game Controller
To install Game Controller on your Ubuntu Linux, you can download the file and do the following :

```shell
chmod 777 installGameController.sh
./installGameController.sh
```

This will then install ssl-game-controller, ssl-status-board, TIGERS AutoRef, ERFORCE AutoRef onto your Home Directory, within the folder : "ssl-software"

If got into any error, please copy or screenshot text and post it in Mattermost Chat, and await for reply. 
