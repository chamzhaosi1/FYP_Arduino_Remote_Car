from django.db import models
from django.contrib.auth.models import User
import os
import time
import random

def generate_random_number():
    current_time = int(time.time())  # Get the current time as a Unix timestamp
    random.seed(current_time)  # Set the random seed based on the current time
    random_number = random.randint(1, 100)  # Generate a random number between 1 and 100
    return random_number

def get_image_path(instance, filename):
    # Custom folder name based on instance attribute
    folder_name = instance.user_id.username  # Assuming user_id is a ForeignKey to the User model
    # To keep the file if same person name
    sub_folder_name = instance.person_name
    # To prevent same image
    file_endwith = generate_random_number()
    # Joining the custom folder name with the filename
    return os.path.join('authorized', folder_name, sub_folder_name, "".join([("-".join([sub_folder_name, str(file_endwith)])), ".jpg"]))

class AuthorizedImg(models.Model):
    authorized_img = models.ImageField(max_length=100, blank=False, null=False, upload_to=get_image_path)
    person_name = models.CharField(max_length=100, null=False)
    uploaded_datetime = models.DateTimeField()
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return str(self.authorized_img)+ " " + self.person_name