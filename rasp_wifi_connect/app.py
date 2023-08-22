"""
Steps to let raspberry pi connect to wifi
1) Once raspberry pi is up and running, run this progrme with comment "flask run"
2) Checking whether the wifi connection is up or down
  - if down then run wifi server bash file to let user connect it and access to the wifi connection html page
    - then run the wifi client bash file with ssid and password as parameters
    - once connected to the wifi, doing the ping again to check whether the successfully or not.
        - if successfully then automatically subcribe a mqtt topic and publish a message "ROMO device (00:11:22:33:44:55) is ready"
        - if unsuccessfully then run again the run wifi server bash file to let user connect it and access to the wifi connection html page
  - if up then directly subcribe a mqtt topic and publish a message "ROMO device (00:11:22:33:44:55) is ready"
"""

from flask import Flask, render_template, redirect, url_for
import subprocess, time, datetime, json, bcrypt, serial, threading
import paho.mqtt.client as mqtt
from flask import request

app = Flask(__name__)

# Define MQTT parameters
broker_address = "w33.kynoci.com"
broker_port = 1883
main_path = "romo"
pub_topic = "device_connect_status"
sub_topic_motor = "ROMO_motor_control"
sub_topic_head = "ROMO_head_control"
sub_topic_hook = "ROMO_hook_control"
username = "newera"
password = "newera2023"

# ping_gateway = "1.1.1.1"
ping_gateway = "192.168.8.1"
# ping_server = "google.com"
ping_server = "192.168.8.83"

ser = serial.Serial("/dev/ttyACM0", baudrate=115200)

LF = 0
RF = 1
LB = 2
RB = 3

tmp_motor_rpm = [0,0,0,0]
cur_motor_rpm = [0,0,0,0]
prev_motor_rpm = [0,0,0,0]

# store wifi list into a array
wifi_list = []

def main():
  print('Main funtion..')

  # if can ping (not lan), call mqttconnect 
  # this prove it already connect wifi previously
  if ping(ping_gateway) and ping (ping_server) :
    mqttSubPub()

  # if cannot get ping
  else:
    refresh_wifi_list()
    # if json is not empty, then read the json file
    try:
      with open('wifi_history.json', 'r') as f:
          data = json.load(f)

      # -1 = not connected yet
      # 0 = unsuccessfully connected
      # 1 = successfully connected
      wifi_connected_status = -1

      global wifi_list
    
      for i in range(len(data)):
        ssid = data[i]['ssid']
        password = data[i]['password']

        # if the ssid is in the list, then run the wifi client bash file with ssid and password as parameters
        if ssid in wifi_list:
          # run wifi client bash file with ssid and password as parameters
          run_wifi_client_bash(ssid, password)   

          for j in range(5):
            if not ping(ping_gateway) and not ping (ping_server):
              print(f"Trying ping...{j}")
              wifi_connected_status = 0
              time.sleep(5)
            else:
              print(f"Ping success, start mqtt...{j}")
              wifi_connected_status = 1
              time.sleep(5)
              mqttSubPub()

        # If not avaliable wifi in wifi list, then wifi server will be restarted again  
        if wifi_connected_status == -1:
          print(wifi_connected_status)

          # stop the wifi client first
          stop_run_wifi_client_bash()
          
          # run wifi server bash file again
          run_wifi_server_bash()

        ## If loop 5 time cannot get ping, then wifi server will be restarted again  
        elif wifi_connected_status == 0:
          print(wifi_connected_status)
          # stop the wifi client first
          stop_run_wifi_client_bash()

          # run wifi server bash file again
          run_wifi_server_bash()
          
    except (FileNotFoundError, json.decoder.JSONDecodeError):
      # if there is do not wifi history record
        print("FileNotFoundError")

        # stop the wifi client first
        stop_run_wifi_client_bash()

        # run wifi server bash file
        run_wifi_server_bash()

# method get and return wifi submit html file
@app.route('/')
def list_wifi():
  # print("list_ping above")
  # if don't get ping then list out the file let user manually connect to the wifi
  if not ping(ping_gateway) and not ping (ping_server):

    print("list_ping below")

    global wifi_list

    # print(wifi_list)
    return render_template('connect_wifi.html', wifi_list=wifi_list)

  else:
    # Get current date and time
    now = datetime.datetime.now()

    # return the date and time in a specific format
    return render_template('connect_wifi.html', message="WIFI has been connected ( " + now.strftime("%Y-%m-%d %H:%M:%S") +" )")
  

@app.route('/connect_wifi', methods=['POST'])
def connect_wifi(): 
  if request.method == 'POST':
    # get the ssid and password from the html form
    ssid = request.form['ssid']
    password = request.form['wifi_password']

    global wifi_list

    # if ssid not in the list and password is invalid
    if ssid not in wifi_list or password == "":
      return render_template('connect_wifi.html', error="Invalid SSID or password")

    # stop the wifi server first
    stop_run_wifi_server_bash()

    # run wifi client bash file with ssid and password as parameters
    run_wifi_client_bash(ssid, password)

    # variable to keep wifi connection good or not
    # 0 = not good, 1 = good
    wifi_connected_status = 0

    # loop 5 time ping if not get ping
    for i in range(5):
      if not ping(ping_gateway) and not ping (ping_server):
        k = i+1
        print(f"After connecting WIFI cannot get ping: {k}")
        wifi_connected_status = 0
        time.sleep(5)
      else:
        print(f"After connecting WIFI get ping and start mqtt")
        wifi_connected_status = 1
        save_wifi_info(ssid, password)

        # connect to mqtt server and subcribe/public a topic
        mqttSubPub()

        break 
    """ 
    if the wifi connection good then program will be stuck at function mqttConnent()
    once it finished, that means the wifi is diconnection need connect again 
    """

    ## If loop 5 time cannot get ping, then wifi server will be restarted again  
    if wifi_connected_status == 0:
      # stop the wifi client first
      stop_run_wifi_client_bash()

      # run wifi server bash file again
      run_wifi_server_bash()
    
  return redirect('/')
  # return None

@app.route('/refresh_wifi', methods=['GET'])
def refresh_wifi():
  print("refresh wifi")
  global wifi_list
  refresh_wifi_list()
  return wifi_list


def refresh_wifi_list():
  print("refresh wifi list")
  global wifi_list

  # get all avaliable wifi 
  scan_wifi()

  # read the file and store it in a list
  wifi_list = retrive_wifi()


def mqttSubPub():
  # checking ping condition
  if ping(ping_gateway) and ping (ping_server):
    client = connect_mqtt()
    # get mac address
    mac_address_command = "sudo ip link show wlan0 | head -n 2 | tail -n 1 | xargs | cut -d ' ' -f 2"
    mac_address = subprocess.check_output(mac_address_command, shell=True).decode('utf-8').strip()
   
    # Create three new thread
    sub_thread = threading.Thread(target=get_data_to_arduino, args=(client, mac_address))
    
    # pub_thread = threading.Thread(target=send_status_to_mqtt, args=(client, mac_address))
    browser_thread = threading.Thread(target=open_browser, args=(mac_address,))
    
    # Start the thread
    sub_thread.start()
    
    # pub_thread.start()
    browser_thread.start()
    holdGetPing()

    # Wait for the thread to finish
    # Once cannot get ping then the process will end 
    # then web server will be start 
    # pub_thread.join()

    # after that, sub mqtt stop thread and browser thread
    # sub_thread.set()
    # browser_thread.join()

def holdGetPing():
  while True:
    # checking ping condition
    if not ping(ping_gateway) and not ping (ping_server):
      break

    # every 5 second check one time
    time.sleep(5)
  
# def send_status_to_mqtt(client ,mac_address):
#   print(mac_address)
#   # Publish a message to the topic
#   # message = "ROMO device (" + mac_address + ") is ready"'
#   i=0
#   j=0
#   while True:
#     # checking ping condition
#     if ping(ping_gateway) and ping (ping_server):
#       i+=1
#       print(f"Get ping: {i}")

#       # if i == 1:
#       #   # run node browser file
#       #   browser_thread = threading.Thread(target=open_browser, args=(mac_address,))
#       #   browser_thread.start()

#       # Get current date and time (timestamp)
#       timestamp = int(time.time() * 1000)
#       message = {
#         "datetime": timestamp, 
#         "mac_address": mac_address
#       }

#       client.publish(main_path+"/"+pub_topic, json.dumps(message))
#       time.sleep(5) ## every 1 minutes publish a message to the topic
#     else:
#       j+=1
#       print(f"Cannot get ping: {j}")
#       # Disconnect from the broker
#       client.disconnect() 

#       # stop the browser thread 
#       # browser_thread.stop()

#       # stop the wifi client first
#       stop_run_wifi_client_bash()

#       # run wifi server bash file again
#       run_wifi_server_bash()
      
#       break

## open browser and access to romo website
def open_browser(mac_address):
  # Create the command list with node, JavaScript file path, and parameter
  # this node browser cannot run as root
  node_command = "runuser -l engineer -c 'node /home/engineer/romo_v2/chromium-browser/index.js" + " " + mac_address + "'"
  # node_command = "node /home/engineer/romo_v2/chromium-browser/index.js" + " " + mac_address
  print(node_command)

  # Run the command and capture the output
  subprocess.check_output(node_command, shell=True)

## subscribe the sub topic to get rmp and direction values
def get_data_to_arduino(client, mac_address):
  print(main_path+"/"+mac_address+"/"+sub_topic_motor)
  client.subscribe(main_path+"/"+mac_address+"/"+sub_topic_motor)
  print(main_path+"/"+mac_address+"/"+sub_topic_head)
  client.subscribe(main_path+"/"+mac_address+"/"+sub_topic_head)
  print(main_path+"/"+mac_address+"/"+sub_topic_head)
  client.subscribe(main_path+"/"+mac_address+"/"+sub_topic_hook)
  # client.loop_forever()

# Define callback function for when the client receives a CONNACK response from the broker
def on_message(client, userdata, msg):
  print(msg.topic) 

  if msg.topic.find("ROMO_motor_control") != -1:
    print("below") 
    global cur_motor_rpm
    global prev_motor_rpm

    mecanum_data = json.loads(msg.payload.decode())
    print(mecanum_data)
    tmp_motor_rpm[LF] = -int(mecanum_data["lf"])
    tmp_motor_rpm[RF] = mecanum_data["rf"]
    tmp_motor_rpm[LB] = -int(mecanum_data["lb"])
    tmp_motor_rpm[RB] = mecanum_data["rb"]

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

    stringValueMotor = str(cur_motor_rpm[LF])+','+str(cur_motor_rpm[RF])+','+str(cur_motor_rpm[LB])+','+str(cur_motor_rpm[RB])+' '
    print(stringValueMotor)

    ## To send data to the arduino
    ser.write(bytes(stringValueMotor, 'ascii'))

  elif msg.topic.find("ROMO_head_control") != -1:
    head_data = json.loads(msg.payload.decode())
    stringValueHead = str(head_data["angle_x"])+","+str(head_data["angle_y"])+' '
    print(stringValueHead)
    ## To send data to the arduino
    ser.write(bytes(stringValueHead, 'ascii'))

  elif msg.topic.find("ROMO_hook_control") != -1:
    hook_data = json.loads(msg.payload.decode())
    stringValueHook = str(hook_data["hook_value"])+' '
    print(stringValueHook)
    ser.write(bytes(stringValueHook, 'ascii'))
  
# Define callback function for when the client successfully connect the mqtt
def on_connect(client, userdata, flags, rc):
  print("Connected with result code " + str(rc))
  
def connect_mqtt():
  # Create a client instance and connect to the broker
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message

  # Set the username and password for authentication
  client.username_pw_set(username, password)
  client.connect(broker_address, broker_port)

  # Start the MQTT client loop in a separate thread
  client.loop_start()
  return client
  

def save_wifi_info(ssid, password):
  new_wifi_info = {
    "ssid": ssid,
    "password": password
  }

  # Check if the file exists or is empty
  try:
    with open('wifi_history.json', 'r') as f:
        data = json.load(f)

  except (FileNotFoundError, json.decoder.JSONDecodeError):
    data = []

  exists = False

  # if wifi info not exist, then just append the new wifi info
  for wifi_info in data:
    if wifi_info["ssid"] == new_wifi_info["ssid"] and wifi_info["password"] == new_wifi_info["password"]:
      exists = True
      break

  if not exists:
    # Append new data to the Python object
    data.append(new_wifi_info)

    # Write the modified Python object back to the JSON file
    with open('wifi_history.json', 'w') as f:
      json.dump(data, f)
  

def scan_wifi():
  # run linux commentrs to get list of wifi networks
  # scan all available wifi surrounding it
  scan_wifi_list_command = "sudo iw dev wlan0 scan | grep 'SSID:' | grep -v 'HESSID' | sed 's/SSID://g'  > wifi_list.txt"
  subprocess.check_output(scan_wifi_list_command, shell=True) 

def retrive_wifi():
  wifi_list = [] 

  # open the file and read the lines
  with open('wifi_list.txt', 'r') as f:
    for line in f:
      # remove the new line character
      line = line.strip() 
      
      # if the line is not empty then continue to the next line
      if line:
        wifi_list.append(line)

  return wifi_list

# Checking whether the host is up or down
def ping(host):
  result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  if result.returncode == 0:
    # if get ping
    return True
  else:
    # if don't get ping
    return False

def run_wifi_server_bash():
  wifi_server_command = "sudo bash /usr/local/sbin/romo_start_wifi_ap.sh"
  subprocess.check_output(wifi_server_command, shell=True)  
  time.sleep(5)

def run_wifi_client_bash(ssid, password):
  # print ssid and password
  print(f"WIFI connecting to ssid: {ssid}, password: {password}")
  print(f"sudo bash /usr/local/sbin/romo_start_wifi_client.sh {ssid} {password}")
  wifi_client_command = "sudo bash /usr/local/sbin/romo_start_wifi_client.sh " + ssid + " " + password
  subprocess.check_output(wifi_client_command, shell=True)
  # python wait for 3 seconds to let the wifi client connect to the wifi
  time.sleep(5)

def stop_run_wifi_server_bash():
  wifi_server_command = "sudo bash /usr/local/sbin/romo_stop_wifi_ap.sh"
  subprocess.check_output(wifi_server_command, shell=True)
  time.sleep(5)

def stop_run_wifi_client_bash():
  wifi_client_command = "sudo bash /usr/local/sbin/romo_stop_wifi_client.sh"
  subprocess.check_output(wifi_client_command, shell=True)
  time.sleep(5)


if __name__ == "app":
  ## To preven the Device or resource busy (-16) error, 
  ## wait for 10 seconds before running the main function 
  time.sleep(10)
  main()

# print("File one __name__ is set to: {}" .format(__name__))
