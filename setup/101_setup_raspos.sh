## Flash Rasberry pi os to micro sd card
wget https://downloads.raspberrypi.org/raspios_lite_arm64/images/raspios_lite_arm64-2022-09-26/2022-09-22-raspios-bullseye-arm64-lite.img.xz
unxz ./2022-09-22-raspios-bullseye-arm64-lite.img.xz
dd if=./2022-09-22-raspios-bullseye-arm64-lite.img of=/dev/sdb bs=1M status=progress

## set root
sudo su -
passwd

rasp-config
# enable ssh
# set wifi

## wifi statip ip
# Current ip address
hostname -I
# gateway
ip r
# DNS
grep "namesever" /etc/resolv.conf

nano /etc/dhcpcd.conf
# interface wlan0
# static_routers=192.168.0.1
# static domain_name_servers=192.168.0.1
# static ip_address=192.168.7.121/24

reboot

apt -y update 
apt -y dist-upgrade
apt -y install curl wget git ssh

# set malaysia time
sudo timedatectl set-timezone Asia/Kuala_Lumpur

