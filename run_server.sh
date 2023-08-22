<!-- P3 : Romo Frontend -->
cd /home/engineer/romo_v2/romo_web/frontend/romo_front/
npm start

<!-- P4 : Romo Backend -->
source /usr/local/bin/venv/bin/activate
cd /home/engineer/romo_v2/romo_web/backend/romo_back
daphne -e ssl:8000:privateKey=/etc/nginx/ssl/kynoci.com-sub-privkey.pem:certKey=/etc/nginx/ssl/kynoci.com-sub-cert.pem romo_back.asgi:application

<!-- P5 : Romo Face recognization -->
source /usr/local/bin/venv/bin/activate 
cd /home/engineer/romo_v2/romo_web/face_recognition
python server.py --cert-file /etc/nginx/ssl/kynoci.com-sub-cert.pem --key-file /etc/nginx/ssl/kynoci.com-sub-privkey.pem

