from django.db import models
# from datetime import datetime  

# class User(models.Model):
#   username = models.CharField(max_length=100, unique=True, null=False)
#   password_encryted = models.CharField(max_length=100, null=False)
#   tool_control = models.SmallIntegerField(null=True)
#   face_recognize = models.BooleanField(null=True)
#   create_datetime = models.DateTimeField(default=datetime.now, blank=True)
  
#   def __str__(self):
#     return self.username + " " + str(self.create_datetime)

# class ROMO(models.Model):
#   mac_address = models.CharField(max_length=100, null=False)
#   romo_label = models.CharField(max_length=100, null=False)
#   status = models.CharField(max_length=50, null=False)
#   last_active = models.DateTimeField()
#   user_id = models.ForeignKey("User", null=True, on_delete=models.CASCADE, related_name='+')

#   def __str__(self):
#     return self.username + " " + str(self.create_datetime)

# class Face_Recognize(models.Model):
#   authorized_img_url = models.CharField(max_length=200, null=False)
#   image_label = models.CharField(max_length=100, null=False)
#   upload_datatime = models.DateTimeField(default=datetime.now, blank=True)
#   user_id = models.ForeignKey("User", null=True, on_delete=models.CASCADE, related_name='+')

#   def __str__(self):
#     return self.image_label + " " + str(self.upload_datatime)

# class Unauthorized(models.Model):
#   unathorized_img_url = models.CharField(max_length=100, null=False)
#   unknown_img_label = models.CharField(max_length=100, null=False)
#   capture_datetime = models.DateTimeField(default=datetime.now, blank=True)
#   user_id = models.ForeignKey("User", null=False, on_delete=models.CASCADE, related_name='+')
#   romo_id = models.ForeignKey("ROMO", null=False, on_delete=models.CASCADE, related_name='+')

#   def __str__(self):
#     return self.unknown_img_label + " " + str(self.capture_datetime)
