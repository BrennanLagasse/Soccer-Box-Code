#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time


if __name__ == '__main__':
    
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyUSB3", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            welcome_message = "{} connected!".format(arduino.port)
            print(welcome_message.encode())
            try:
                while True:
                    # cmd=input("Enter command : ")
                    # arduino.write(cmd.encode())
                    # time.sleep(0.1) #wait for arduino to answer
                    while arduino.inWaiting()==0: pass
                    if  arduino.inWaiting()>0: 
                        answer=arduino.readline()
                        try:
                            print(answer.encode())
                        except:
                            # nothing
                            garbage = True
                        arduino.flushInput() #remove data after reading
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")
