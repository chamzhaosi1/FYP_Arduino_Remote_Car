
# Latest
apt -y install curl gnupg
curl http://nginx.org/keys/nginx_signing.key | apt-key add -
echo "deb http://nginx.org/packages/mainline/debian/ buster nginx" > /etc/apt/sources.list.d/latest-nginx.list
apt -y update
apt-cache policy nginx
apt -y install nginx
/etc/init.d/nginx start
systemctl enable nginx

# Get SSL
mkdir -p /etc/nginx/ssl/
cd /etc/nginx/ssl/
curl -O -k "https://username:password@192.168.0.1/ssl/kynoci.com-sub-privkey.pem"
curl -O -k "https://username:password@192.168.0.1/ssl/kynoci.com-sub-cert.pem"~

