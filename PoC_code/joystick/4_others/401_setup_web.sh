apt -y install nginx
apt -y purge nginx

# Defautl Web Folder @  /var/www/html/

# mkdir -p  /home/engineer/tigaky-romo_v2/joystick/web-folder
# chmod 777 -R /home/engineer/tigaky-romo_v2/joystick/
mkdir -p  /home/engineer/romo_v2/joystick/webfolder
chmod 777 -R /home/engineer/romo_v2/joystick
mkdir /etc/nginx/sites-enabled
cat > /etc/nginx/sites-enabled/default << EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /home/engineer/romo_v2/joystick/webfolder;
    server_name _;
    access_log  /var/log/nginx/default-access.log combined;
    error_log   /var/log/nginx/default-error.log warn;
    index  simulator.html;
    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF

rm -rf /etc/nginx/conf.d/default.conf
cd etc/nginx/sites-enabled
mv default default.conf
mv default.conf /etc/nginx/conf.d/
systemctl restart nginx

/etc/init.d/nginx restart

# mkdir /etc/nginx/sites-available
# mkdir /etc/nginx/sites-enabled
# nano /etc/nginx/nginx.conf

# cat > /etc/nginx/sites-available/default << EOF
# server {
#     listen       80;
#     server_name  localhost;

#         #access_log  logs/host.access.log  main;

#         location / {
#             root   /home/engineer/romo_v2/joystick/webfolder;
#             index  simulator.html;
#         }

#         #error_page  404              /404.html;

#         # redirect server error pages to the static page /50x.html
#         #
#         error_page   500 502 503 504  /50x.html;
#         location = /50x.html {
#             root   html;
#         }
# }
# EOF

# ln -s /etc/nginx/sites-available/default.conf /etc/nginx/sites-enabled
# nginx -s stop && nginx
