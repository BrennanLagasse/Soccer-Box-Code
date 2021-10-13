from gpiozero import Button
import time

NUM_TARGERTS = 2

PIEZOCERAMIC_PINS = [6, 12, 13, 19, 16, 26, 20, 21]

# Event listener
def piezoTriggered(index):
    return lambda: print("Target " + str(index + 1) + " was triggered")


# Create and store Piezoceramic objects
piezoceramics = [] 

for x in range(0, NUM_TARGERTS):
    # Create Piezo object, pull down
    piezoceramics.append(Button(PIEZOCERAMIC_PINS[x], True)) 
    
    # ^ None = floating
    # ^ True = v not reversed, None = ?

    # Add event listener
    piezoceramics[x].when_pressed = piezoTriggered(x)

    

while True:
    print("Still active")
    time.sleep(10)
