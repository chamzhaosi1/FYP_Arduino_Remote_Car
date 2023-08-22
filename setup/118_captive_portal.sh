# Refer: https://pimylifeup.com/raspberry-pi-captive-portal/
sudo apt -y update
sudo apt -y upgrade

sudo apt -y install git libmicrohttpd-dev build-essential

cd ~
git clone https://github.com/nodogsplash/nodogsplash.git

cd ~/nodogsplash
make
sudo make install

sudo nano /etc/nodogsplash/nodogsplash.conf

# Tells what interface the nodogsplash software should show up on and what address it should be listening on.
GatewayInterface wlan0
GatewayAddress 192.168.5.1 // same as the wifi ap ip address
GatewayPort 8088
MaxClients 250
AuthIdleTimeout 480

sudo /root/nodogsplash/nodogsplash
chmod +x /root/nodogsplash/nodogsplash

chmod 777 /etc/nodogsplash/htdocs/splash.html

sudo nano /etc/nodogsplash/htdocs/splash.html
# add redirect code to head point to our customs website
# <meta http-equiv="refresh" content="0; URL='http://raspberrypi:5000/'" />

sudo nano /etc/rc.local
# nodogsplash

sudo service nodogsplash start
sudo service nodogsplash stop


cat > /etc/systemd/system/nodogsplash.service << EOF
[Unit]
Description=Captive portal for Raspberry Pi
After=network.target

[Service]
ExecStart=/root/nodogsplash/nodogsplash

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable nodogsplash
sudo systemctl start nodogsplash
sudo systemctl restart nodogsplash 
sudo systemctl stop nodogsplash
sudo systemctl disable nodogsplash
sudo systemctl status nodogsplash

sudo journalctl -u nodogsplash  


