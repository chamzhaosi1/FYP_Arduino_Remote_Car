# python 3.6

import random
import serial, time, json
from paho.mqtt import client as mqtt_client
import ssl

ser = serial.Serial("/dev/ttyACM0", baudrate=115200)

BROKER = 'w33.kynoci.com'
PORT = 1883
TOPIC = "romo/e4:5f:01:42:52:3e/ROMO_motor_control"
# TOPIC = "python*"
# generate client ID with pub prefix randomly
# CLIENT_ID = "python-mqtt-wss-sub-{id}".format(id=random.randint(0, 1000))
USERNAME = 'babi'
PASSWORD = 'chu'

LF = 0
RF = 1
LB = 2
RB = 3

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

    mecanum_data = json.loads(msg.payload.decode())
    print(mecanum_data)
    tmp_motor_rpm[LF] = -int(mecanum_data["lf"])
    tmp_motor_rpm[RF] = mecanum_data["rf"]
    tmp_motor_rpm[LB] = -int(mecanum_data["lb"])
    tmp_motor_rpm[RB] = mecanum_data["rb"]
    
    
    # if(msg.topic=='mecanum/lf'):
    #     # print("Left Front {}".format(msg.payload.decode()))
    #     tmp_motor_rpm[FR] = -int(msg.payload.decode())
    #     # print(FR)

    # if(msg.topic=='mecanum/rf'):
    #     # print("Right Front {}".format(msg.payload.decode()))
    #     tmp_motor_rpm[FL]= int(msg.payload.decode())
    #     # print(FL)

    # if(msg.topic=='mecanum/lb'):
    #     # print("Left Back {}".format(msg.payload.decode()))
    #     tmp_motor_rpm[BR] = -int(msg.payload.decode())
    #     # print(BR)

    # if(msg.topic=='mecanum/rb'):
    #     # print("Right Back {}".format(msg.payload.decode()))
    #     tmp_motor_rpm[BL] = int(msg.payload.decode())
    #     # print(BL)
    
    if (abs(tmp_motor_rpm[LF] - prev_motor_rpm[LF]) > 10 or tmp_motor_rpm[LF] == 0):
        cur_motor_rpm[LF] = tmp_motor_rpm[LF]
        prev_motor_rpm[LF] = cur_motor_rpm[LF]

    if (abs(tmp_motor_rpm[RF] - prev_motor_rpm[RF]) > 10 or tmp_motor_rpm[RF] == 0):
        cur_motor_rpm[RF] = tmp_motor_rpm[RF]
        prev_motor_rpm[RF] = cur_motor_rpm[RF]

    if (abs(tmp_motor_rpm[LB] - prev_motor_rpm[LB]) > 10 or tmp_motor_rpm[LB] == 0):
        cur_motor_rpm[LB] = tmp_motor_rpm[LB]
        prev_motor_rpm[LB] = cur_motor_rpm[LB]

    if (abs(tmp_motor_rpm[RB] - prev_motor_rpm[RB]) > 10 or tmp_motor_rpm[RB] == 0):
        cur_motor_rpm[RB] = tmp_motor_rpm[RB]
        prev_motor_rpm[RB] = cur_motor_rpm[RB]


    stringValaue = str(cur_motor_rpm[LF])+','+str(cur_motor_rpm[RF])+','+str(cur_motor_rpm[LB])+','+str(cur_motor_rpm[RB])+' '
    print(stringValaue)
    ser.write(bytes(stringValaue, 'ascii'))

def connect_mqtt():
    # client = mqtt_client.Client(CLIENT_ID, transport='websockets')
    client = mqtt_client.Client()
    # client.tls_set(ca_certs='/etc/ssl/certs/ca-certificates.crt')

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