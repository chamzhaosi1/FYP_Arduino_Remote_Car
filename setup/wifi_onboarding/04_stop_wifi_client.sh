cat > /usr/local/sbin/romo_stop_wifi_client.sh << EEOOFF
rm -rf /etc/systemd/system/wpa_supplicant.service
systemctl disable wpa_supplicant.service
systemctl stop wpa_supplicant.service

## We need enanble this service then just able to remove it from random ip address
systemctl enable hostapd
systemctl start hostapd

sleep 1

systemctl stop hostapd
systemctl disable hostapd
EEOOFF
chmod +x /usr/local/sbin/romo_stop_wifi_client.sh
bash /usr/local/sbin/romo_stop_wifi_client.sh
ip a