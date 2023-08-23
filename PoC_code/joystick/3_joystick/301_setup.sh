date -s '2023-03-15 13:27:56'

cat > /etc/apt/sources.list << EOF
deb http://ftp.jp.debian.org/debian/ bullseye main contrib non-free
deb http://ftp.jp.debian.org/debian/ bullseye-updates main contrib non-free
deb http://ftp.jp.debian.org/debian bullseye-backports main contrib non-free
EOF
apt -y update && apt -y dist-upgrade

apt -y install joystick python3-pygame
jstest --event /dev/input/js0
jstest /dev/input/js0
pip install pygame

###############################################################################
### 
###############################################################################
pip install paho-mqtt