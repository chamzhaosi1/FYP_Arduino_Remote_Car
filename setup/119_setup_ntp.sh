# ## Setup NTP
# su -
# apt-get update -y
# apt-get -y remove ntp
# apt-get -y install ntp
# cat >> /etc/ntp.conf << EOF

# server 0.pool.ntp.org iburst
# server 1.pool.ntp.org iburst
# server 2.pool.ntp.org iburst
# server 3.pool.ntp.org iburst

# restrict 192.168.8.0 netmask 255.255.255.0 nomodify notrap

# EOF


# update-rc.d ntp defaults
# update-rc.d ntp enable
# update-rc.d ntp disable

# systemctl unmask ntp.service
# service ntp restart
# service ntp start
# service ntp status
# service ntp stop
# service ntp disable
# # systemctl enable ntp.service
# # systemctl restart ntp.service
# # systemctl status ntp.service

# # check status
# ntpq -p

# ########################################################################

# ## For other device use
# su -
# apt-get update -y
# apt-get -y install ntp

# cat >> /etc/ntp.conf << EOF
# server 192.168.8.138 iburst
# EOF

# service ntp restart
# # systemctl restart ntp 
# service ntp start
# service ntp status
# service ntp stop
# cat /var/log/syslog
# cat /var/log/messages

# # check status
# watch -n 1 ntpq -p 

# watch -n 1 date

# timedatectl

# ## testing 

# date -s "2023-5-01 08:34:56"

# ################################################################
# su -
# apt -y update
apt -y install chrony

cat >> /etc/chrony/chrony.conf << EOF 

# Comment out external NTP servers
# server 0.debian.pool.ntp.org iburst
local stratum 10

# Specify the subnet or IP range of your local network to allow access.
# Replace 192.168.8.0/24 with your actual subnet.
allow 192.168.8.0/24

# Use the system's hardware clock as the reference source.
# refclock PHC /dev/ptp0 poll 3 dpoll -2 offset 0

EOF

systemctl unmask chrony
systemctl restart chrony
systemctl stop chrony
systemctl disable  chrony
systemctl status chrony
systemctl enable chrony
<<<<<<< HEAD
# apt -y remove chrony

chronyc tracking

>>>>>>> cecf365db7b2b0b9885eb3d2690469ebcc289e22
#####################################################

apt -y update
apt -y install chrony

cat >> /etc/chrony/chrony.conf << EOF 

# Use Debian vendor zone.
# pool 2.debian.pool.ntp.org iburst

#Add your local server configuration (replace with your own server address)
server romo.kynoci.com iburst

log tracking measurements statistics

EOF

systemctl restart chrony 
systemctl enable chrony
systemctl status chrony
# systemctl restart ufw
# systemctl status ufw

# systemctl stop chrony
# rm /var/lib/chrony/chrony.drift
# systemctl start chrony

# tail - n 50 /var/log/chrony/chrony.log
# ls /var/log/chrony

journalctl -u chrony.service -b
# journalctl -u chrony -xe 

watch -n 1 chronyc tracking

watch -n 1 date 

###################################################
# apt -y install iptables-persistent

# iptables -L
# iptables -A INPUT -p udp --dport 123 -j ACCEPT
# netfilter-persistent save
# iptables-save > /etc/iptables/rules.v4 




