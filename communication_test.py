import serial,time
from rpi_ws281x import *

# LED info
LED_PIN = 18
LED_COUNT      = 264
LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 100
LED_INVERT     = False
LED_CHANNEL    = 0
LED_PER_TARGET = 33
NUM_TARGETS = 8

# Tnitialize and start RGB lights
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Define functions which animate LEDs in various ways.
def color_wipe(strip, color, target, index):
    """Wipe color across display a pixel at a time"""
    i = target*LED_PER_TARGET + index

    strip.setPixelColor(i, color)
    strip.show()

def fill_all(strip, color, target):
    """Instantly change color of pixels in target range"""
    start = target*LED_PER_TARGET
    for i in range(start, start + LED_PER_TARGET):
        strip.setPixelColor(i, color)
    strip.show()

def reset_all(strip):
    """Reset all of the LEDs in the smart box"""
    for target in range(0, NUM_TARGETS):
        fill_all(strip, BLACK, target)


if __name__ == '__main__':
    
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                target = 0
                index = 0
                reset = False

                while True:
                    

                    if(reset):
                        fill_all(strip, Color(255, 0, 0), target)
                        reset = False
                        index = 0
                    elif(index < 33):
                        i = target*LED_PER_TARGET + index
                        strip.setPixelColor(i, Color(0,0,0))
                        strip.show()
                        index += 1
                    else:
                        reset = True
                    
                        
                    while(arduino.inWaiting() > 0): 
                        answer = arduino.readline()
                        i = int(answer)
                        print(answer)

                        if(i == target):
                            reset = True

                        arduino.flushInput() #remove data after reading

                    time.sleep(.05)

            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")