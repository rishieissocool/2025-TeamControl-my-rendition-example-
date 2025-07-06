import mmap
import os
import time

SHARED_MEM = "/udp_shared_mem"
BUFFER_SIZE = 8192

def process_message(message):
    """Process the latest valid message."""
    print(f"[{time.time()}] Processing:", message)

def read_shared_memory():
    with open(f"/dev/shm{SHARED_MEM}", "r+b") as shm:
        mmapped = mmap.mmap(shm.fileno(), BUFFER_SIZE, access=mmap.ACCESS_READ)
        last_message = ""

        while True:
            mmapped.seek(0)  # Always read from start
            message = mmapped.read(BUFFER_SIZE).decode().strip()

            if message and message != last_message:
                last_message = message
                process_message(last_message)

            time.sleep(0.0001)  # Prevent CPU overuse

if __name__ == "__main__":
    read_shared_memory()
