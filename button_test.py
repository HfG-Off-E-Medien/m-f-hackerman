from keyboard import is_pressed
import cv2
from grove.factory import Factory
from grove.grove_led import GroveLed

# Buttons
button1 = Factory.getButton("GPIO-HIGH", 5)
button2 = Factory.getButton("GPIO-HIGH", 6)

while True:
    cv2.waitKey(1)
    if not button1.is_pressed():
        while True:
            if button1.is_pressed():
                print("blau");
                break
    if not button2.is_pressed():
        while True:
            if button2.is_pressed():
                print("red");
                break