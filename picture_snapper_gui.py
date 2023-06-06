# ----------------------------------------------------------------------------- #
# Imports

from picamera import PiCamera
from time import sleep
from keyboard import is_pressed
import socket
from tcp_funcs import *
from patcher import Patcher
from utils import flush_dir
import tkinter as tk
from PIL import Image
from PIL import ImageTk
from time import sleep

# ----------------------------------------------------------------------------- #
# Args

HOST = "172.20.10.12"
PORT = 4454
BUFFER_SIZE = 1024
CACHE_IMG_PATH = '/home/pi/Desktop/moritz_filter/cache/tmp.jpg'
CACHE_PATCHES_PATH = '/home/pi/Desktop/moritz_filter/cache/patches/'

# ----------------------------------------------------------------------------- #
# Modules

camera = PiCamera()
P = Patcher(output_dir = CACHE_PATCHES_PATH)


# ----------------------------------------------------------------------------- #
# GUI

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display")
        self.root.geometry("480x320")
        
        self.button = tk.Button(root, text="JOY", command=self.procedure, height=460, width=300)
        self.button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def procedure(self):
        # Take picture
        print('picture taken.')
        camera.capture(CACHE_IMG_PATH)
                
        # Hide the button
        self.button.place_forget()
        
        # Load and display the image
        image = Image.open(CACHE_IMG_PATH)
        image = image.resize((self.root.winfo_width(), self.root.winfo_height()))
        photo = ImageTk.PhotoImage(image)
        
        self.label = tk.Label(self.root, image=photo)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label.image = photo
        self.root.update()
        
        # Empty patches cache
        flush_dir(CACHE_PATCHES_PATH)

        # Split image into patches
        P.split_image_into_patches(CACHE_IMG_PATH)
        
        self.root.after(5000, self.restore_state)
    
    def restore_state(self):
        self.label.place_forget()
        self.button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

"""
def procedure():

    
    image = Image.open(CACHE_IMG_PATH)
    image = image.resize((480,320))
    tk_image = ImageTk.PhotoImage(image)
    
    label.configure(image=tk_image)
    label.image = tk_image
    
    root.update()
    sleep(5)

    label.configure(image=None)
    label.image=None

        

root = tk.Tk()
root.geometry("480x320")

label = tk.Label(root)
label.pack()

button = tk.Button(root, text="Display Image", command=procedure)
button.pack(pady=20)

root.mainloop()
"""