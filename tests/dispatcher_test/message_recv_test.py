from TeamControl.network.receiver import Receiver
IP = "127.0.0.1"
PORT_NUMBER = 50514

def main():
    recv = Receiver(ip=IP,port=PORT_NUMBER)
    print(f"RECEIVER CREATED @ {recv.addr}")
    while True:
        message,addr = recv.listen()
        print(f"message {message} recv from {addr}")
        
main()