###########################################################################################
### Phase 1 : Basic AMQP
###########################################################################################

cat > /etc/apt/sources.list << EOF
deb http://mirror.0x.sg/debian/ bullseye main contrib non-free
# deb-src http://mirror.0x.sg/debian/ bullseye main contrib non-free
deb http://security.debian.org/debian-security bullseye-security main contrib non-free
# deb-src http://security.debian.org/debian-security bullseye-security main contrib non-free
deb http://mirror.0x.sg/debian/ bullseye-updates main contrib non-free
# deb-src http://mirror.0x.sg/debian/ bullseye-updates main contrib non-free
EOF
apt -y update && apt -y dist-upgrade

apt install curl gnupg apt-transport-https -y

## Team RabbitMQ's main signing key
# curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | gpg --dearmor | tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null
## Launchpad PPA that provides modern Erlang releases
# curl -1sLf "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xf77f1eda57ebb1cc" | gpg --dearmor | tee /usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg > /dev/null
## PackageCloud RabbitMQ repository
curl -1sLf "https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey" | gpg --dearmor | tee /usr/share/keyrings/io.packagecloud.rabbitmq.gpg > /dev/null

apt-cache policy erlang

wget https://packages.erlang-solutions.com/erlang-solutions_2.0_all.deb
apt install ./erlang-solutions_2.0_all.deb
apt update

## Add apt repositories maintained by Team RabbitMQ
tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
## Provides modern Erlang/OTP releases
##
## "bionic" as distribution name should work for any reasonably recent Ubuntu or Debian release.
## See the release to distribution mapping table in RabbitMQ doc guides to learn more.
# deb [signed-by=/usr/share/keyrings/io.packagecloud.rabbitmq.gpg] https://packagecloud.io/rabbitmq/erlang/debian/ bullseye main
# deb-src [signed-by=/usr/share/keyrings/io.packagecloud.rabbitmq.gpg] https://packagecloud.io/rabbitmq/erlang/debian/ bullseye main

## Provides RabbitMQ
##
## "bionic" as distribution name should work for any reasonably recent Ubuntu or Debian release.
## See the release to distribution mapping table in RabbitMQ doc guides to learn more.
deb [signed-by=/usr/share/keyrings/io.packagecloud.rabbitmq.gpg] https://packagecloud.io/rabbitmq/rabbitmq-server/debian/ bullseye main
deb-src [signed-by=/usr/share/keyrings/io.packagecloud.rabbitmq.gpg] https://packagecloud.io/rabbitmq/rabbitmq-server/debian/ bullseye main
EOF

## Update package indices
apt update -y

## Install Erlang packages
apt install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl
erl --verasion

## Install rabbitmq-server and its dependencies
apt install rabbitmq-server -y --fix-missing



### Step 7 : # Enable Management
rabbitmq-plugins enable rabbitmq_management
rabbitmqctl add_user username password
rabbitmqctl set_user_tags username administrator
rabbitmqctl set_permissions -p / username ".*" ".*" ".*"

### Step 8 : # Enable Move Queue
rabbitmq-plugins enable rabbitmq_shovel rabbitmq_shovel_management

										  # Web Portal      - 15672
										  # (AMQP)          -  5672
                                          
###########################################################################################
### Phase 2 : Additional MQTT
###########################################################################################

rabbitmq-plugins enable rabbitmq_mqtt     # (HTTP or HTTPS) -  
rabbitmq-plugins enable rabbitmq_web_mqtt # (WS or WSS)		- 15675


### Step 9 : Restart
service rabbitmq-server restart
rabbitmqctl "report"
# rabbitmqctl "reset"

rabbitmqctl add_user newera newera2023
rabbitmqctl set_permissions -p / newera ".*" ".*" ".*"
rabbitmqctl set_user_tags newera management

http://tzx.maco.my:15672/


###############################################################################
### To fix too many File Open
###############################################################################

### As ROOT : Fix Error
# "Visual Studio Code is unable to watch for file changes in this large workspace" (error ENOSPC)#
# https://code.visualstudio.com/docs/setup/linux#_visual-studio-code-is-unable-to-watch-for-file-changes-in-this-large-workspace-error-enospc
cat /proc/sys/fs/inotify/max_user_watches
cat >> /etc/sysctl.conf << EOF
fs.inotify.max_user_watches=524288
EOF
sysctl -p