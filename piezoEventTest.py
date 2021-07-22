from gpiozero import Button
import time

NUM_TARGERTS = 8

PIEZOCERAMIC_PINS = [6, 12, 13, 19, 16, 26, 20, 21]

def piezoTriggered(index):
    return lambda: print("Target " + str(index + 1) + " was triggered")


# Create and store Piezoceramic objects
piezoceramics = [] 

for x in range(0, NUM_TARGERTS):
    piezoceramics.append(Button(PIEZOCERAMIC_PINS[x]))
    piezoceramics[x].when_pressed = piezoTriggered(x)

while True:
    time.sleep(100)
