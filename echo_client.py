# echo-client.py

import socket
from os.path import getsize

HOST = 
PORT =
BUFFER_SIZE = 1024

def send_file(server, BUFFER_SIZE, FILENAME):
    filesize = getsize(FILENAME)
    print("Sending file with following size: ", filesize)
    server.send(f"{filesize}".encode())
    with open(FILENAME, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                return True
            server.sendall(bytes_read)
        #progress.update(len(bytes_read))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    send_file(s, BUFFER_SIZE, "hello.txt")
    """
    s.sendall(b"Hello, world")
    data = s.recv(1024)
    """
