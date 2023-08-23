import pygame
import random
from paho.mqtt import client as mqtt_client
import ssl
import time

import os
import sys
os.environ["SDL_VIDEODRIVER"] = "dummy"

BROKER = 'w33.kynoci.com'
PORT = 1883
TOPIC = "joystick/#"
# CLIENT_ID = "python-mqtt-wss-sub-{id}".format(id=random.randint(0, 1000))
USERNAME = 'babi'
PASSWORD = 'chu'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )

def on_message(client, userdata, msg):
    print("Received `{payload}` from `{topic}` topic".format(
        payload=msg.payload.decode(), topic=msg.topic))

def connect_mqtt():
    # client = mqtt_client.Client(CLIENT_ID, transport='websockets')
    client = mqtt_client.Client()
    # client.tls_set(ca_certs='/etc/ssl/certs/ca-certificates.crt')

    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client


pygame.init()

num_joysticks = pygame.joystick.get_count()
print("Number of joysticks: {}".format(num_joysticks))

joystick = pygame.joystick.Joystick(0)
joystick.init()

client = connect_mqtt()

while True:
    pygame.event.get()
    # Get the input values for the Xbox gamepad axes
    axis_x = round(joystick.get_axis(0)*100)
    tmp = (joystick.get_axis(1)-0.0305)*100
    if(tmp>=0):
        tmp=tmp*100/97
    else:
        tmp=tmp*100/103

    axis_y = -round(tmp)
    # Get the input values for the Xbox gamepad buttons
    # button_a = joystick.get_button(0)
    # button_b = joystick.get_button(1)
    # button_x = joystick.get_button(2)
    # button_y = joystick.get_button(3)
    # Print the input values
    # print("X-axis: {}, Y-axis: {}, A: {}, B: {}, X: {}, Y: {}".format(
    #     axis_x, axis_y, button_a, button_b, button_x, button_y))
    # Print the input values
    print("X-axis: {}, Y-axis: {}".format(axis_x, axis_y))
    print("X-axis: {}, Y-axis: {}".format(joystick.get_axis(2), joystick.get_axis(3)))

    client.publish("joystick/x",axis_x)
    client.publish("joystick/y",axis_y)
    time.sleep(0.1)
