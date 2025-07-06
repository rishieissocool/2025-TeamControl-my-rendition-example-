## Receiver here for game controller
from TeamControl.SSL.proto2 import ssl_gc_referee_message_pb2
from TeamControl.network.receiver import Multicast

class GameControllerReceiver(Multicast):
    def __init__(self) -> None:
        group : str = '224.23.2.2'
        port : int = 10003
        decoder = ssl_gc_referee_message_pb2.Referee()
        buffer_size : int = 6000
        timeout : float = 5.0
        super().__init__(port=port, group=group, decoder=decoder, buffer_size=buffer_size,timeout=timeout)
        
    def listen(self) -> ssl_gc_referee_message_pb2.Referee:
        # see Multicast listen(), decode()
        return super().listen()
    
    