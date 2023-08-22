from django.db import models
from django.contrib.auth.models import User

class ROMO(models.Model):
  mac_address = models.CharField(max_length=100, null=False, unique=True)
  romo_label = models.CharField(max_length=100, null=False)
  status = models.CharField(max_length=50, null=False)
  last_active = models.DateTimeField()
  user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='+')

  def __str__(self):
    return self.romo_label + " " + str(self.last_active)
