cat > /usr/local/sbin/romo_stop_wifi_ap.sh << EEOOFF
systemctl stop hostapd
systemctl disable hostapd

systemctl stop dnsmasq
systemctl disable dnsmasq

cat /root/dhcpcd.conf_ori > /etc/dhcpcd.conf
cat > /root/iptables_stop.rules << EOF
#!/bin/sh
### delete all existing rules.
/sbin/iptables -F
/sbin/iptables -t nat -F
/sbin/iptables -t mangle -F
/sbin/iptables -X
exit
EOF
bash /root/iptables_stop.rules
EEOOFF

chmod +x /usr/local/sbin/romo_stop_wifi_ap.sh 
bash /usr/local/sbin/romo_stop_wifi_ap.sh 