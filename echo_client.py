# echo-client.py

import socket
from tcp_funcs import *

HOST = "172.20.10.11"
PORT = 4454
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    send_file(s, BUFFER_SIZE, "Rothwald.jpg")
    _ = receive_file(s, BUFFER_SIZE, "server_answer.jpg")