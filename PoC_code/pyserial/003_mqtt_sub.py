# python 3.6

import random
import serial, time
from paho.mqtt import client as mqtt_client
import ssl

ser = serial.Serial("/dev/ttyACM0", baudrate=115200)

BROKER = 'lim.kynoci.com'
PORT = 8083
TOPIC = "mecanum/#"
# TOPIC = "python*"
# generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-wss-sub-{id}".format(id=random.randint(0, 1000))
USERNAME = 'babi'
PASSWORD = 'chu'

FR = 0
FL = 1
BR = 2
BL = 3

tmp_motor_rpm = [0,0,0,0]
cur_motor_rpm = [0,0,0,0]
prev_motor_rpm = [0,0,0,0] 

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )



def on_message(client, userdata, msg):
    global cur_motor_rpm
    global prev_motor_rpm
    
    if(msg.topic=='mecanum/lf'):
        # print("Left Front {}".format(msg.payload.decode()))
        tmp_motor_rpm[FR] = -int(msg.payload.decode())
        # print(FR)

    if(msg.topic=='mecanum/rf'):
        # print("Right Front {}".format(msg.payload.decode()))
        tmp_motor_rpm[FL]= int(msg.payload.decode())
        # print(FL)

    if(msg.topic=='mecanum/lb'):
        # print("Left Back {}".format(msg.payload.decode()))
        tmp_motor_rpm[BR] = -int(msg.payload.decode())
        # print(BR)

    if(msg.topic=='mecanum/rb'):
        # print("Right Back {}".format(msg.payload.decode()))
        tmp_motor_rpm[BL] = int(msg.payload.decode())
        # print(BL)
    
    if (abs(tmp_motor_rpm[FR] - prev_motor_rpm[FR]) > 10 or tmp_motor_rpm[FR] == 0):
        cur_motor_rpm[FR] = tmp_motor_rpm[FR]
        prev_motor_rpm[FR] = cur_motor_rpm[FR]

    if (abs(tmp_motor_rpm[FL] - prev_motor_rpm[FL]) > 10 or tmp_motor_rpm[FR] == 0):
        cur_motor_rpm[FL] = tmp_motor_rpm[FL]
        prev_motor_rpm[FL] = cur_motor_rpm[FL]

    if (abs(tmp_motor_rpm[BR] - prev_motor_rpm[BR]) > 10 or tmp_motor_rpm[FR] == 0):
        cur_motor_rpm[BR] = tmp_motor_rpm[BR]
        prev_motor_rpm[BR] = cur_motor_rpm[BR]

    if (abs(tmp_motor_rpm[BL] - prev_motor_rpm[BL]) > 10 or tmp_motor_rpm[FR] == 0):
        cur_motor_rpm[BL] = tmp_motor_rpm[BL]
        prev_motor_rpm[BL] = cur_motor_rpm[BL]


    stringValaue = str(cur_motor_rpm[FR])+','+str(cur_motor_rpm[FL])+','+str(cur_motor_rpm[BR])+','+str(cur_motor_rpm[BL])+' '
    print(stringValaue)
    ser.write(bytes(stringValaue, 'ascii'))

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID, transport='websockets')
    client.tls_set(ca_certs='/etc/ssl/certs/ca-certificates.crt')

    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client


def run():
    client = connect_mqtt()
    client.loop_forever()


if __name__ == '__main__':
    run()