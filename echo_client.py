# echo-client.py

import socket
from os.path import getsize

HOST = 
PORT =  

def send_file(server, FILENAME):
    filesize = getsize(FILENAME)
    print(filesize)
    server.send(f"{filesize}".encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    send_file(s, "hello.txt")
    """
    s.sendall(b"Hello, world")
    data = s.recv(1024)
    """
