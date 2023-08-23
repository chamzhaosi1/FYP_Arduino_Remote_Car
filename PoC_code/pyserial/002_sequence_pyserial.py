import serial, time

ser = serial.Serial("/dev/ttyACM0", baudrate=115200)
print(ser.name) 

# ser.write(command.encode(encoding = 'ascii', errors = 'strict'))
ser.write(b'0,0,0,0 ')
time.sleep(5)
ser.write(b'-50,50,50,-50 ')
time.sleep(5)
ser.write(b'0,0,0,0 ')
time.sleep(5)
ser.write(b'-100,100,-100,100 ')
time.sleep(5)
ser.write(b'0,0,0,0 ')
time.sleep(5)
ser.write(b'-50,50,-100,100 ')
