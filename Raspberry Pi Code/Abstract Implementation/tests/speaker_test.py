#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time


if __name__ == '__main__':
    """Goes through all the speakers and makes a test sound"""
    
    serial_connections = []
    serial_connections.append(serial.Serial("/dev/ttyUSB0", 9600, timeout=1))
    serial_connections.append(serial.Serial("/dev/ttyUSB1", 9600, timeout=1))
    serial_connections.append(serial.Serial("/dev/ttyUSB2", 9600, timeout=1))
    serial_connections.append(serial.Serial("/dev/ttyUSB3", 9600, timeout=1))

    # Reset serial logs
    for i in range(len(serial_connections)):
        serial_connections[i].reset_input_buffer()

    for i in range(0, len(serial_connections)):
        serial_connections[i].write("red\n")
        time.sleep(1)