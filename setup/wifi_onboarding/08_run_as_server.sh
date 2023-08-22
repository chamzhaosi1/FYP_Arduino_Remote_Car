## AS ROOT
su -
cd /home/engineer/romo_v2/romo_web/rasp_wifi_connect

chmod +x start_up_run.sh

cat > /etc/systemd/system/rasp_wifi_connect.service << EOF
[Unit]
Description=Raspberry Wifi Connection Service
After=network.target

[Service]
User=root
ExecStart=/home/engineer/romo_v2/romo_web/rasp_wifi_connect/start_up_run.sh

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable rasp_wifi_connect
sudo systemctl start rasp_wifi_connect
sudo systemctl restart rasp_wifi_connect
sudo systemctl status rasp_wifi_connect    
sudo systemctl stop rasp_wifi_connect
sudo systemctl disable rasp_wifi_connect

sudo journalctl -u rasp_wifi_connect            
