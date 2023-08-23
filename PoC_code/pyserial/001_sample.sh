#  pip install pyserial
# https://pyserial.readthedocs.io/en/latest/shortintro.html

import serial
import time
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

arduino.write(bytes(x, 'utf-8'))

sio.write(unicode("hello\n"))
ser.write("run MODE-55\r\n")


https://pyserial.readthedocs.io/en/latest/shortintro.html
