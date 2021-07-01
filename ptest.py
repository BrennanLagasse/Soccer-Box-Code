from gpiozero import Button

import time

button = Button(21)

while True:
    if button.is_pressed:
        print("Button currently pressed." + time.time())
