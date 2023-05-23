# ----------------------------------------------------------------------------- #
# Imports

import cv2
#from time import sleep
from keyboard import is_pressed
import socket
from tcp_funcs import *
from patcher import Patcher
from utils import flush_dir
import time
import numpy as np
from subprocess import Popen

# ----------------------------------------------------------------------------- #
# Args

HOST = input("type in server ip")#"172.20.10.11"
PORT = 
BUFFER_SIZE = 1
CACHE_IMG_PATH = '/home/pi/Desktop/.../cache/tmp.jpg'
CACHE_PATCHES_PATH = '/home/pi/Desktop/.../cache/patches/'

# Hide the mouse
Popen(['unclutter', '-idle', '0.01', '-root'])

# ----------------------------------------------------------------------------- #
# Modules

P = Patcher(output_dir = CACHE_PATCHES_PATH)

# ----------------------------------------------------------------------------- #
# Run Main loop
print('loop is running...')
cap = cv2.VideoCapture(0)
cv2.namedWindow('video', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (480, 320))
    cv2.imshow('video', frame)

    # Wait for user to press q - then picture is snapped and procedure started.
    if cv2.waitKey(1) % 0xFF == ord('q'):
        print('picture taken.')
        
        # Empty patches cache
        flush_dir(CACHE_PATCHES_PATH)
        
        # Split image into patches
        patches_paths = P.split_image_into_patches(frame)
        
        # Connect to server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
            # Send amount of patches to be transmitted to the server
            num_patches = len(patches_paths)
            
            s.sendall(int_to_32_byte(num_patches).encode("utf-8"))
            
            # Send patches over to the server
            for patch_path in patches_paths:
                send_file(s, BUFFER_SIZE, patch_path)
            
            black = np.zeros(frame.shape).astype(np.uint8)
            for i in range(8):
                cv2.imshow('video', black)
                cv2.waitKey(500)
                cv2.imshow('video', frame)
                cv2.waitKey(500)
            
            _ = receive_file(s, BUFFER_SIZE, "server_answer.jpg")
            
            frame = cv2.imread("server_answer.jpg")
            cv2.imshow('video', frame)
            while True:
                if cv2.waitKey(1) % 0xFF == ord('q'):
                    break
            
    if cv2.waitKey(1) % 0xFF == ord('c'):
        break
        

    #sleep(0.05)
