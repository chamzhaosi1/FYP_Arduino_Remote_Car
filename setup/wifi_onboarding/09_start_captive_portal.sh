cat > /usr/local/sbin/romo_start_captive_portal.sh << EEOOFF
#!/bin/bash
sudo /root/nodogsplash/nodogsplash
EEOOFF

chmod +x /usr/local/sbin/romo_start_captive_portal.sh 
bash /usr/local/sbin/romo_start_captive_portal.sh 