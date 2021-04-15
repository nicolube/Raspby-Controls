import os
import serial
import json
import sys
import glob

import usb.core
import usb.util
from usb.legacy import CLASS_MASS_STORAGE

from os import path
import os

__dir = path.dirname(path.realpath(__file__))

config = {}
for file in os.listdir(path.join(__dir, "configs")):
    raw = open(path.join(__dir, "configs", file), "r").read()
    config[file.split('.')[0]] = json.loads(raw)

def drives():
    if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        files = os.listdir("/media")
        for file in files:
            print(file)
        return files
    return []

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
