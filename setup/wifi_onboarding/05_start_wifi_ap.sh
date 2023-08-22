cat > /usr/local/sbin/romo_start_wifi_ap.sh << EEOOFF
### Setup WLAN0 interface
rfkill unblock wifi

cat > /etc/dhcpcd.conf << EOF
# At the bottom, paste this:
interface wlan0
static ip_address=192.168.5.1/24
nohook wpa_supplicant
EOF

### Config Hostapd
cat > /etc/hostapd/hostapd.conf << EOF
interface=wlan0
driver=nl80211
ssid=romo_wifi
wpa_passphrase=newera2023
hw_mode=g
channel=4
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

### Auto Run Hostapd as a Services
systemctl enable hostapd
systemctl start hostapd

systemctl enable dnsmasq
systemctl start dnsmasq

### Share LAN Internet
cat > /root/iptables_shared_lan.rules << EOF
#!/bin/sh
### delete all existing rules.
/sbin/iptables -F
/sbin/iptables -t nat -F
/sbin/iptables -t mangle -F
/sbin/iptables -X
### shared WAN for LAN
/bin/echo 1 > /proc/sys/net/ipv4/ip_forward
/sbin/iptables --table nat -A POSTROUTING -o eth0 -j MASQUERADE
/sbin/iptables -P FORWARD ACCEPT
exit
EOF
bash /root/iptables_shared_lan.rules
EEOOFF

chmod +x /usr/local/sbin/romo_start_wifi_ap.sh
bash /usr/local/sbin/romo_start_wifi_ap.sh