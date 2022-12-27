#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time
import sys


if __name__ == '__main__':

    time.sleep(1)
    
    print(sys.argv[1]) # prints var1
    print(sys.argv[2]) # prints var2

