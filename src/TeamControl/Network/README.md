# NETWORK

This directory includes the Server - Client Communication.

Server Class includes the server as an object that establish a connection to the Robot Client

## Server Class

When the server has been initialed, the server will broadcast itself over the network.

The server will also have an active reciving UDP socket to allow the Robots to try to connect to the server.

If there is an Incoming UDP message, the Server will first check if the robot has a "robot_id".

If the robot sends the message without a "robot_id", we will assume that it is a new robot.

Thus, it will continue onto an ID assignation proceedure *This might be updated in the future*

After an ID has been assigned, the Server will then store all relevant data into a [RobotCli] Object. 

Afterwards, The server will be then responsible for regularly requesting PING checks.

As well as sending individual robot [Actions] and [Game Commands], etc.


---
PING Checks : Sending PING commands over then network and demand Robots to report back telemetry data.