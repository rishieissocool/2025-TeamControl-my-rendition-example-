import socket
import time

PORT = 9999
BUFFER_SIZE = 8192
FLAG = "[FLAG]"

def process_message(message):
    """Process the latest valid message."""
    print(f"[{time.time()}] Processing:", message)

def udp_receiver():
    """Receive UDP packets and process flagged messages."""
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))
    
    print(f"Listening for UDP packets on port {PORT}...")

    while True:
        message, addr = sock.recvfrom(BUFFER_SIZE)
        message = message.decode().strip()

        if FLAG in message:
            process_message(message)

if __name__ == "__main__":
    udp_receiver()
import socket
import time

PORT = 9999
BUFFER_SIZE = 8192
FLAG = "[FLAG]"

def process_message(message):
    """Process the latest valid message."""
    print(f"[{time.time()}] Processing:", message)

def udp_receiver():
    """Receive UDP packets and process flagged messages."""
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))
    
    print(f"Listening for UDP packets on port {PORT}...")

    while True:
        message, addr = sock.recvfrom(BUFFER_SIZE)
        message = message.decode().strip()

        if FLAG in message:
            process_message(message)

if __name__ == "__main__":
    udp_receiver()