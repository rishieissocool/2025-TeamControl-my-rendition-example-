import socket

UDP_IP = "127.0.0.1"  # Localhost (or use the server's IP address)
UDP_PORT = 9999
MESSAGE = "[FLAG] This is a test message."

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send data
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

print(f"Message sent to {UDP_IP}:{UDP_PORT}")