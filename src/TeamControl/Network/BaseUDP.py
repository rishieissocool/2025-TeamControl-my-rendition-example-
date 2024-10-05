
import socket
import sys
import time
import random
import os 
import ast

#enum
import enum
from enum import auto

# Log
import logging
log = logging.getLogger()
log.setLevel(logging.NOTSET)

class UDP(enum.IntEnum):
    SOCK_BROADCAST_UDP = auto()
    SOCK_UDP = auto()
    SOCK_MULTICAST_UDP = auto()

class BaseSocket(): 
    """
    base class of receiver and sender
    provides common base functions
    """
    def __init__(self,ip: str=None, port: int=0, sock_type=UDP.SOCK_UDP,buffer_size: int=1024, binding=True):
        """BaseSocket - initials simple UDP socket as a base for receiver and sender class

        Args:
            ip (str, optional): IP address of device. Defaults to None.
            port (int, optional): Port number for socket communication. Defaults to 0.
            sock_type (UDP, optional): Type of UDP Socket (Please use UDP Class). Defaults to UDP.SOCK_UDP.
            binding (bool, optional): Do you want to bind this socket ? (recommended for reusable socket). Defaults to True.
        """
        if ip is None:
            self.ip:str = self._obtain_sys_ip()
        elif isinstance(ip,str): 
            self.ip:str = ip
        else:
            log.critical(f"{ip=} is not string, current type: {type(ip)}")
            
        if isinstance(port,int):
            self.port:int = port
        else:
            log.critical(f"{port=} is not int, current type:{type(port)}")
        
        if sock_type is UDP.SOCK_UDP or sock_type is UDP.SOCK_BROADCAST_UDP:
            self.sock:socket.socket = self._setup_socket(sock_type)
        if binding:
            self.ready = self._bind_sock()
        else:
            self.isReady:bool = True
        
        self.buffer_size = buffer_size
        self.source:tuple[str,int] = None
        self.destination:tuple[str,int] = None
        
        log.debug(f"{self.__class__.__name__} socket is now active on {self.ip},{self.port}")
        
 
    def _bind_sock(self) -> bool:
        """
        Binds the socket to it's ip and a port
        Params:
            isBinded (bool) : boolean determining whether the socket has been binded successfully
            port (int) : check and auto generated port number
            tries (int) : number of tries before aborting

        Returns:
            bool: 
                returns isBinded to self.ready
        """
        isBinded = False
        tries = 0
        while not isBinded or tries > 3:
            try: #binding with IP and Port
                if self.port == 0: 
                    port = self._generate_port()
                else: # since self.port is provided, use self.port
                    port = self.port 
                
                # binds socket to ip and port
                self.sock.bind((self.ip,port))
                
                # if bind is successful, updating new port
                self.port:int = port
                
                # the socket is now binded
                isBinded = True 
                
            # if there is a value error : STOP     
            except ValueError as ve:
                raise ValueError("ERROR : ",ve)
                
            # if there is a socket error, probably something to do with binding, continue
            except socket.error as se:
                log.debug(f"Uable to bind at port: {port}, trying again... \nfull message : '{se}'\n ")
                tries += 1 
            
            except Exception as e: 
                log.error("Socket cannot be created, ",e)
                raise Exception(f"Error encountered, aborting ... \n {e}")
                
            finally:
                log.debug("socket is binded : ",isBinded)
                
        return isBinded # this can be either true or false
    
    
    def listen(self,duration: int=None)-> str|None:
        """Default Listen function
            Listening on Receiving Socket 
            *THIS IS NOT A LOOP*

        Args:
            duration (int, optional): time(second) to listen to port. Defaults to None.

        Returns:
            str : decoded data 
            or nothing.
        Raises: 
            socket.error : Socket is Not ready, please create socket again
            socket.timeout : Socket duration ended
        """
        data = None
        if not self.ready: #terminates
            log.error("Socket is not ready ? Please check and intialise socket")
        
        if duration is not None:
            self.sock.settimeout(duration)
        else:
            self.sock.settimeout(None)
        
        try:
            log.debug(f"{self.__class__.__name__} sock is now listening with buffersize : {self.buffer_size}")
            data, addr = self.sock.recvfrom(self.buffer_size)
            # data received
        except socket.timeout as to:
            #socket timeout
            log.info("Duration ended : ",to)
            data = None
        finally:
           if data is not None: # return anything that has a value
                decoded_data = self._decode(data)
                log.debug(f"Message Recieved from {addr=}, {decoded_data}")
                return decoded_data
            
    
    def _decode(self,data:bytes) ->str|bytes:
        """Default Decode Function (internal, not to be called)
        Args:
            data (bytes): Byte data received over UDP
        Returns:
            bytes: data that cannot be decoded
                or
            str: Decoded data using utf-8
        """
        try : 
            decoded_data = data.decode('utf-8')
        except UnicodeDecodeError as ude : 
            log.warning("cannot decode data, returning original. \n",ude)
            return data
        finally:
            return decoded_data        
        
    
    def send(self, msg : bytes|str, duration : int=None, destination:tuple[str,int] = None)-> None:
        """
        sends message to sender's destination

        Args:
            msg (bytes | str): the message that you want to send, can be in bytes or string format.
            duration (int, optional): How long do you want to send this message for. Defaults to None -> No repeats.
            destination (tuple[str,int],optional): Other location you want to send. Defaults to None -> use sender's destination address.

        Raises:
            AttributeError: No destination addr found. Either update sending socket, or send in a new destination.
        """
        if not self.ready:
            log.error("Sender is not ready")
            raise ValueError("Please check and initialise sender.")
        
        if self.destination is None and destination is None:
            raise AttributeError(f"Destination : {self.destination=} | {destination=}")
        elif isinstance(destination,tuple):
            self.destination = destination
        elif isinstance(destination,str):
            destination = ast.literal_eval(destination)
            
        # if the message is a string, it encodes message
        if isinstance(msg,str):
            msg = bytes(msg.encode('utf-8'))
        
        # if user input a duration value
        if duration is not None:
            endTime = time.time()+duration
        else :
            endTime = time.time()

        
        # reset sent boolean
        sent = False
        while not sent: # loop for sending message
            try:
                self.sock.sendto(msg,self.destination)
                sent = True
            except socket.error as se:
                log.critical(se)    
            
            finally:
                log.debug(f"message {msg.decode()} is sent to destination {self.destination}: {sent}")
                
                if endTime - time.time() <= 0:
                    log.info("Duration ended")
                    break #exit loop
                else:
                    sent = False # try again
        
                
    def close(self):
        """ Close the socket """
        self.sock.close()  
     
    @staticmethod
    def _setup_socket(type) -> socket.socket:
        """ Initialise socket
        Initailise socket for broadcasting in UDP
        Arg = 
        UDP.SOCK_BROADCAST_UDP = broadcast
        UDP.SOCK_UDP = udp 
        UDP.SOCK_MULTICAST_UDP = multicast

        Returns:
            socket.socket: returns the initailised socket
        """
        if type == UDP.SOCK_BROADCAST_UDP:
            broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            return broadcast
        elif type == UDP.SOCK_UDP: 
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return udp
        elif type == UDP.SOCK_MULTICAST_UDP:
            multicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            multicast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            multicast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            
            
        
    @staticmethod
    def _obtain_sys_ip() -> str:
        """
        Obtaining system's ip address *This may not work in Arch linux
        
        Params:
            os_system(sys.platform) =  current os_system.
        
        Raises:
            ValueError: No matching os system, cannot obtain IP, will need to input manually.

        Returns:
            ip (str): system's ip address
        """
        os_system = sys.platform
        match os_system:
            case 'win32':
                ip = socket.gethostbyname(socket.gethostname())
            case 'linux':
                ip = os.popen('hostname -I').read().strip().split(" ")[0]
                print(os.popen('hostname -I').read().strip().split(" "))
            case 'darwin':
                ip = os.popen('ipconfig getifaddr en0').read().strip()
            case _:
                raise ValueError("Cannot Obtain IP, Please input ip address manually")       
        return ip
    
    @staticmethod
    def _generate_port() -> int:
        port = random.randint(5000, 9000)
        log.debug(f"port generated : {port}")
        return port

  
    