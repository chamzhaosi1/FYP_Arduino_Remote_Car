import paho.mqtt.client as mqtt

broker = "lim.kynoci.com"
port = 8083

client = mqtt.Client()
client.ws_set_options(path="/mqtt")

websocket_url = "lim.kynoci.com"
client.ws_set_options(path="/mqtt", headers={"Sec-WebSocket-Protocol": "mqtt"}, url=websocket_url)

username = "babi"
password = "chu"
client.username_pw_set(username, password)

client.connect(broker, port)

topic = "your/topic"
message = "your message"
client.publish(topic, message)

client.disconnect()