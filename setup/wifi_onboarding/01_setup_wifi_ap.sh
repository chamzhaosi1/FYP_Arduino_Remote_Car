# Refer: https://www.diyhobi.com/setup-a-wireless-access-point-on-raspberry-pi-4-os-lite/

apt -y update && apt -y dist-upgrade
apt -y install rpi-eeprom
rpi-eeprom-update -a
# *** INSTALLING EEPROM UPDATES ***
# BOOTLOADER: update available
#    CURRENT: Thu 29 Apr 16:11:25 UTC 2021 (1619712685)
#     LATEST: Wed 11 Jan 17:40:52 UTC 2023 (1673458852)
#    RELEASE: default (/lib/firmware/raspberrypi/bootloader/default)
#             Use raspi-config to change the release.
#   VL805_FW: Using bootloader EEPROM
#      VL805: up to date
#    CURRENT: 000138a1
#     LATEST: 000138a1
#    CURRENT: Thu 29 Apr 16:11:25 UTC 2021 (1619712685)
#     UPDATE: Wed 11 Jan 17:40:52 UTC 2023 (1673458852)
#     BOOTFS: /boot
# Using recovery.bin for EEPROM update
# EEPROM updates pending. Please reboot to apply the update.
# To cancel a pending update run "sudo rpi-eeprom-update -r".

# Tune WLAN0 interface
rfkill unblock wifi

# Backup
cp /etc/dhcpcd.conf /root/dhcpcd.conf_ori

# Enable Default WiFi AP's IP Address
cat > /etc/dhcpcd.conf << EOF
# At the bottom, paste this:
interface wlan0
static ip_address=192.168.5.1/24
nohook wpa_supplicant
EOF
reboot

# Install Hostapd
apt -y install hostapd

# Config Hostapd
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
cat > /etc/default/hostapd << EOF
DAEMON_CONF="/etc/hostapd/hostapd.conf"
EOF

### Manual Run Hostapd
hostapd /etc/hostapd/hostapd.conf

### Auto Run Hostapd as a Services
systemctl unmask hostapd
systemctl enable hostapd
systemctl start hostapd
systemctl restart hostapd
# systemctl stop hostapd
systemctl status hostapd

#########################################################
### Step 2 : Share Network
#########################################################

### Install DHCP Server (Not going to used it as DNS server)
apt -y install dnsmasq
systemctl stop dnsmasq
cat > /etc/dnsmasq.conf << EOF
interface=wlan0
dhcp-range=192.168.5.2,192.168.5.50,255.255.255.0,24h
domain=wlan
address=/gw.wlan/192.168.5.1
EOF
systemctl enable dnsmasq
systemctl start dnsmasq
systemctl restart dnsmasq
systemctl status dnsmasq

### Share LAN Internet
cat > /root/iptables.rules << EOF
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
cat >> /etc/rc.local << EOF
bash /root/iptables.rules
EOF
