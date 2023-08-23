# REFER : https://www.howtoforge.com/how-to-install-mosquitto-mqtt-message-broker-on-debian-11/

### Step 1 : Enable Remote Terminal
apt -y install ssh

### Step 2 : Update System
apt -y update
apt -y dist-upgrade

### Step 3 : Install MQTT Server without Password
apt -y install mosquitto
systemctl is-enabled mosquitto
systemctl status mosquitto

### Step 4 : Install MQTT Client 
apt -y install mosquitto-clients


### Test 1 - Without Password
# At 1st terminal
mosquitto_sub -h localhost -t test
# At 2nd terminal
mosquitto_pub -h localhost -t test -m "Hello from terminal 2"
mosquitto_pub -h localhost -t test -m "Hello from terminal 2 - Publisher"
mosquitto_pub -h localhost -t test -m "Hello"

### Step 5 : Enable MTQQ Server with Password
mosquitto_passwd -c /etc/mosquitto/.passwd babi
# username : babi
# password : chu
cat > /etc/mosquitto/conf.d/auth.conf << EOF
listener 1883
allow_anonymous false
password_file /etc/mosquitto/.passwd
EOF
systemctl restart mosquitto
ss -tunpl

### Test 2 - With Password
# At 1st terminal
mosquitto_sub -h localhost -t test -u "babi" -P "chu"
# At 2nd terminal
mosquitto_pub -h localhost -t "test" -m "Malaysiaiiii " \
    -u "babi" -P "chu"
# At MWTT Explorer

### Step 6 : Enable MTQQ Server with Password and Certificate
apt -y install openssl
openssl dhparam -out /etc/mosquitto/certs/dhparam.pem 2048
cat /etc/shadow
chown -R mosquitto: /etc/mosquitto/certs

# Copy Letencrypt Certifacte
mkdir -p /etc/mosquitto/certs/lim.kynoci.com
cd /etc/mosquitto/certs/lim.kynoci.com/
scp -P 2201 engineer@3ky.my:/home/engineer/lim/* ./

# Config
cat > /etc/mosquitto/conf.d/ssl.conf << EOF
listener 8883
certfile /etc/mosquitto/certs/lim.kynoci.com/fullchain.pem
cafile /etc/mosquitto/certs/lim.kynoci.com/chain.pem
keyfile /etc/mosquitto/certs/lim.kynoci.com/privkey.pem
dhparamfile /etc/mosquitto/certs/dhparam.pem
EOF
systemctl restart mosquitto

## TEST 3
apt -y install ca-certificates
# at 1st Terminal
mosquitto_sub -h localhost -t test -u "babi" -P "chu"
# at 2nd Terminal
mosquitto_pub -h lim.kynoci.com -t test \
    -m "hello again - with SSL enabled 2222" -p 8883 \
    --capath /etc/ssl/certs/ -u "babi" -P "chu"

### Step 7 : Enable MTQQ Server with Password, Certificate and WebSocket
cat > /etc/mosquitto/conf.d/websockets.conf << EOF
listener 8083
protocol websockets
certfile /etc/mosquitto/certs/lim.kynoci.com/fullchain.pem
cafile /etc/mosquitto/certs/lim.kynoci.com/chain.pem
keyfile /etc/mosquitto/certs/lim.kynoci.com/privkey.pem
EOF
systemctl stop  mosquitto
ss -tunpl
systemctl restart mosquitto

tail -f /var/log/mosquitto/mosquitto.log
