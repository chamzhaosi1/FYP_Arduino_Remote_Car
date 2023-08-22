cat > /usr/local/sbin/romo_start_wifi_client.sh << EEOOFF
first_argument="\$1"
second_argument="\$2"
echo "First argument-SSID: \$first_argument"
echo "Second argument-PASS: \$second_argument"

cat /root/dhcpcd.conf_ori > /etc/dhcpcd.conf
wpa_passphrase \$1 \$2 > /etc/wpa_supplicant/wpa_supplicant.conf
cat > /etc/systemd/system/wpa_supplicant.service << EOF       
[Unit]
Description=WPA supplicant
Before=network.target
After=dbus.service
Wants=network.target
IgnoreOnIsolate=true

[Service]
Type=dbus
BusName=fi.w1.wpa_supplicant1
ExecStart=/sbin/wpa_supplicant -u -s -c /etc/wpa_supplicant/wpa_supplicant.conf -i wlan0

[Install]
WantedBy=multi-user.target
Alias=dbus-fi.w1.wpa_supplicant1.service
EOF
systemctl enable wpa_supplicant.service
systemctl start wpa_supplicant

# Static IP configuration
cat > /etc/dhcpcd.conf << EOF
interface wlan0
static ip_address=192.168.8.66/24
static routers=192.168.8.1
EOF

# Restart the networking service
systemctl restart networking.service

EEOOFF

chmod +x /usr/local/sbin/romo_start_wifi_client.sh
bash /usr/local/sbin/romo_start_wifi_client.sh marzuki anakperantau
ip a | grep -v 'inet6\|valid_lft'