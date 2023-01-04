#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time


if __name__ == '__main__':

    time.sleep(1)

    ser = serial.Serial("/dev/ttyUSB2", 9600, timeout=1)
    ser.reset_input_buffer()

    while True:

        while(ser.in_waiting > 0):
            print("I got a message:")
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
