""" Receiver - Socket
This file includes : 
1. Receiver - Basic UDP receiver w/ Recieving Functions (exc. sending)
2. Broadcast - USP Broadcast receiver 
3. Multicast - UDP Multicast receiver
"""
import socket
import struct
import time

from TeamControl.network.baseUDP import BaseSocket,SocketType

#logging
import logging
log = logging.getLogger()
log.setLevel(logging.INFO)

class Receiver(BaseSocket):
    def __init__(self, type=SocketType.SOCK_UDP, ip = None, port = 0, buffer_size = 1024,timeout=1):
        super().__init__(type=type, ip=ip, port=port, binding=True) #UDP must Bind
        self.buffer_size = buffer_size
        self.timeout=timeout
        self.sock.settimeout(timeout)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__} - recv @ {self.addr}, available = {self.is_ready}, {self.timeout=}"
    
    
    def listen(self,duration:float = 0.) -> tuple[str, tuple[str, int]] | None:
        """
        Listens for incoming UDP messages. Returns the message and sender address.
        """
        assert self.is_ready, "Socket is not initialized. try another port ?"
        active = True
        result = '', 0
        if duration !=0 : 
            endTime = time.time() + duration
        else:
            endTime = time.time()     
        while active:
            try:
                message, addr = self.sock.recvfrom(self.buffer_size)
                self.last_message = self._decode(message)
                self.last_addr = addr
                result = self.last_message, self.last_addr
                active = False
            except socket.timeout:
                # print("timeout")
                continue
            
            if time.time() >= endTime:
                return result
                

    def _decode(self,data:bytes):
        try:
            decoded_data = data.decode()
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"cannot decode {data} with default 'utf-8'")
        return decoded_data

class Broadcast(Receiver):
    """reciever for broadcast"""
    def __init__(self, port: int = 0, buffer_size: int = 1024):
        ip = "0.0.0.0" #this is the broadcast address
        type = SocketType.SOCK_BROADCAST_UDP
        super().__init__(ip=ip,port=port,type=type,buffer_size=buffer_size)
        
    

# Multicast Receiver
class Multicast(Receiver):
    def __init__(self,port: int, group:str, decoder:object, buffer_size: int = 6000,timeout:int=0.5) -> None:
        """
        Initialising Multicast socket

        Args:
            decoder (object): SSL Protobuf file and descriptor to decode data
            ip (str, optional): ip of Device trying to connect. Defaults to None -> self obtain device ip.
                                if wanted to connect externally, please type in ip string 
            port (int, optional): port of connection. Defaults to 0 -> auto generated.
            group (str, optional): Mulitcast group. Defaults to "224.5.0.0" -> nothing.
            buffer_size (int, optional): buffer_size for listening. Defaults to 6000. 

        Raises:
            Exception: Needed decoder
        """
        super().__init__(ip="",port=port,type=SocketType.SOCK_MULTICAST_UDP,buffer_size=buffer_size,timeout=timeout)
        
        self.group : str = group
        self.decoder:object = decoder
        self._add_group()
            
    
    def _add_group(self):
        """adds group to multicast socket"""
        self.is_ready = False
        mreq = struct.pack("=4sl", socket.inet_aton(self.group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.is_ready = True
        
    def listen(self) -> str | None: # modified to have decoded data to be boolean
        return super().listen()
    
    def _decode(self,data:bytes) -> bool:
        """
        Reading and decoding the data (overrides super)

        Args:
            data (bytes): data received from listen ()

        Returns:
            str: decoded data
        """
        # Decode with Protobuf 
        # try:
        decoded_data:str= self.decoder.FromString(data) 
        return decoded_data
    

if __name__ == "__main__":
    recv = Receiver(port = 50514)
    b_recv = Broadcast()
    m_recv = Multicast(10006, "224.24.5.3", '')
    while True:
        print("receiver is listening")
        msg,_ = recv.listen()
        print(msg)
        # print("broadcast is listening")
        # b_recv.listen()
        # print("multicast is listening")
        # m_recv.listen()