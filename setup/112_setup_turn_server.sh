# ssh -p 2203 engineer@103.111.75.247

# REFER : https://gabrieltanner.org/blog/turn-server/

apt-get update -y
apt -y install coturn

cat /etc/default/coturn

cat > /etc/default/coturn << EOF
TURNSERVER_ENABLED=1
EOF
systemctl restart coturn

mv /etc/turnserver.conf /etc/turnserver.conf.backup


cat > /etc/turnserver.conf << EOF
# TURN server name and realm
# realm=turn.kynoci.com
# server-name=m1-deb

# IPs the TURN server listens to
listening-ip=0.0.0.0
# External IP-Address of the TURN server
# external-ip=103.111.75.247

# Main listening port
listening-port=3478
# Further ports that are open for communication
min-port=10000
max-port=20000

# Use fingerprint in TURN message
fingerprint
# Log file path
log-file=/var/log/turnserver.log
# Enable verbose logging
verbose

# Specify the user for the TURN authentification
user=test:test123
# Enable long-term credential mechanism
lt-cred-mech

EOF
service coturn restart
service coturn status
systemctl restart coturn 

https://webrtc.github.io/samples/src/content/peerconnection/trickle-ice/?ref=gabriel-tanner

# STUN or TURN URI    : turn:103.111.75.247:3478
# TURN username       : test
# TURN password       : test123
