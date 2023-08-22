apt install avahi-daemon avahi-utils

sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
sudo systemctl status avahi-daemon

sudo nano /etc/hostname
# raspberrypi

sudo nano /etc/hosts
# 192.168.4.1     raspberrypi