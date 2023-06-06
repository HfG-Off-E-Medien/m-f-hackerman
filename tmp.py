"""
from thermal_printer import *

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 240
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
PRINTER_WIDTH = 640
PRINTER_HEIGHT = 384
PRINTER_SIZE = (PRINTER_WIDTH, PRINTER_HEIGHT)
FILE_WIDTH = PRINTER_WIDTH*2
FILE_HEIGHT = PRINTER_HEIGHT*2
FILE_SIZE = (FILE_WIDTH, FILE_HEIGHT)

def printImageFile(filename):
    print('prints ', filename)
    # resize to printer resolution and send to printer
    try:
        image = Image.open(filename)
        im_width, im_height = image.size
        if im_width > im_height:
            image = image.rotate(90, expand=1)
            im_width, im_height = image.size
        ratio = (PRINTER_HEIGHT/float(im_width))
        height = int((float(im_height)*float(ratio)))
        image = image.resize((PRINTER_HEIGHT, height), Image.ANTIALIAS)
        
        printer.printImage(image, False)
        printer.justify('C')
        printer.setSize('S')
        printer.println("PolaPi-Zero")
        printer.feed(3)
    except IOError:
        print ("cannot identify image file", filename)

printer = Adafruit_Thermal(, 115200, timeout=0, rtscts=True)
print("printer built.")

printImageFile("/home/pi/Desktop/moritz_filter/cache/patches/0.jpg")
"""

import serial
uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3000)

import adafruit_thermal_printer
ThermalPrinter = adafruit_thermal_printer.get_printer_class(1.06)

printer = ThermalPrinter(uart)
print(printer)
printer.test_page()
print('done')
printer.feed(2)
