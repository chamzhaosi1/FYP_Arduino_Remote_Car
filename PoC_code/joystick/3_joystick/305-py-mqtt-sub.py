# python 3.6

import random

from paho.mqtt import client as mqtt_client
import ssl

BROKER = 'lim.kynoci.com'
PORT = 8083
TOPIC = "mecanum/#"
# TOPIC = "python*"
# generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-wss-sub-{id}".format(id=random.randint(0, 1000))
USERNAME = 'babi'
PASSWORD = 'chu'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def on_message(client, userdata, msg):

    if(msg.topic=='mecanum/lf'):
        print("Left Front {}".format(msg.payload.decode()))

    if(msg.topic=='mecanum/rf'):
        print("Right Front {}".format(msg.payload.decode()))

    if(msg.topic=='mecanum/lb'):
        print("Left Back {}".format(msg.payload.decode()))

    if(msg.topic=='mecanum/rb'):
        print("Right Back {}".format(msg.payload.decode()))

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