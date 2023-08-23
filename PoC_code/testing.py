import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "romo_back.settings")
django_project_path = "/home/engineer/romo_v2/romo_web/backend/romo_back/romo_back"
sys.path.append(django_project_path)

import django
django.setup()

# Example usage:
from authorized.models import AuthorizedImg
objects = AuthorizedImg.objects.all()
for obj in objects:
    print(obj)



