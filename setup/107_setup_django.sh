source /usr/local/bin/venv/bin/activate

pip install django
pip install djangorestframework
pip install django-rest-knox
pip install --upgrade pip

# cd /home/engineer/romo/live_streaming/backend
cd /home/engineer/romo_v2/django_restfull
django-admin startproject learn_API

# list all command
django-admin