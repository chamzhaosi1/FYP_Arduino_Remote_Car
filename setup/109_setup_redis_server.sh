#Refer: https://cloudinfrastructureservices.co.uk/how-to-install-redis-server-on-debian-11/

apt-get install redis-server -y

apt-cache policy redis-server

systemctl status redis-server
systemctl stop redis-server
systemctl start redis-server

# daphne -e ssl:8080:privateKey=/etc/nginx/ssl/kynoci.com-sub.key:certKey=/etc/nginx/ssl/kynoci.com-sub.crt live_streaming.asgi:application

