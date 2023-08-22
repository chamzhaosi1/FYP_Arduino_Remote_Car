# Install
apt -y install wpasupplicant

# Restore
cat /root/dhcpcd.conf_ori > /etc/dhcpcd.conf

# Config
wpa_passphrase marzuki anakperantau > /etc/wpa_supplicant/wpa_supplicant.conf
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
# systemctl enable wpa_supplicant.service
# systemctl disable wpa_supplicant.service
systemctl start wpa_supplicant
systemctl status wpa_supplicant
