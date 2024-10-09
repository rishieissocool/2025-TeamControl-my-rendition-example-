# NETWORK

This directory includes the Server - Client Communication.

For Communication Protocol please see [Coms]()

Base UDP is the default socket setup for both Receiver and Sender

[SSL_Networking] includes the socket used for SSL_League softwares.


--- 
DEFAULT IP AND PORTS : 
game Controller broadcast 
group : 224.5.23.1
port : 10003

---
Vision in SSL - Vision 
type : multicast UDP
group : 224.5.23.2
port : 10006

---
Vision in GRSim (Default) 
type : multicast UDP
group : 224.5.23.2
port : 10020

---
Vision Tracker Multicast 
group : 224.5.23.2 
port : 10010

Auto-Ref
ip : local
port : 10007
trusted-keeys-dir : config/trusted_keys/auto_ref


Team 
ip: local
port : 10008
trusted-keys-dir: config/trusted_keys/team


remote control 
ip : local 
port : 10011
trusted-keys-dir: config/trusted_keys/remote-control


game controller Continuous Integration (CI)
ip : local
port : 10009