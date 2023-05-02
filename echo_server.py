# echo-server.py

import socket
from tcp_funcs import *
from pipeline import pipeline

HOST = 
PORT = 
BUFFER_SIZE = 1024

print("Setting up tensorflow pipeline...")
P = Pipeline()
P.warump()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        print('Server listening...')
            
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        with conn:
            _ = receive_file(conn, BUFFER_SIZE, 'empfangen.jpg')
            print("processing image...")
            P.run('empfangen.jpg', "processed.jpg")
            send_file(conn, BUFFER_SIZE, 'processed.jpg')
