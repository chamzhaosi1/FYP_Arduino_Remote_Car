import paho.mqtt.client as mqtt
import json

class MQTT_Class:
  def __init__(self):
    self.BROKEN = "w33.kynoci.com"
    self.PORT = 1883
    self.USERNAME = "babi"
    self.PASSWORD = "chu"
    self.mqtt_connect()

  def on_connect(self, client, userdata, flags, rc):
      print("Connected with result code "+str(rc))

  def mqtt_connect(self):
    self.client = mqtt.Client()
    self.client.on_connect = self.on_connect
    self.client.username_pw_set(self.USERNAME, self.PASSWORD)
    self.client.connect(self.BROKEN, self.PORT)
    # Start the MQTT network loop (blocking function)
    # self.client.loop_forever() 
  
  def public_message(self, path, message):
    # message = {"warning": message}
    self.client.publish(path, json.dumps(message))