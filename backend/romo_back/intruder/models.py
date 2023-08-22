from django.db import models
from django.contrib.auth.models import User
from romos.models import ROMO
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
    # Get image name
    intruder_label_id = instance.intruder_label_id
    # Joining the custom folder name with the 
    intruderFolderPath = os.path.join('intrusion', folder_name, intruder_label_id)
    # Add the "media" header folder
    complIntrFldPath =  os.path.join('media', intruderFolderPath)
    # If the intruder folder exist, then
    if os.path.exists(complIntrFldPath):
        # get all image list
        intrImgList = os.listdir(complIntrFldPath)
        # and get the lenght of list
        lenIntrImgList = len(intrImgList)
        # if the intr image is more than 3, then
        if lenIntrImgList > 2:
            # delete the most early one
            os.remove(os.path.join(complIntrFldPath, intrImgList[-1]))
        # set the picture name with length plus 1
        intr_img_label_id = "_".join([intruder_label_id, str(lenIntrImgList+1)])
        return os.path.join('intrusion', folder_name, intruder_label_id, "".join([intr_img_label_id, ".jpg"]))
    else:
       # If the folder don't exist, then initial label the picture name with 1
       return os.path.join('intrusion', folder_name, intruder_label_id, "".join([intruder_label_id, "_1.jpg"])) 
    
    # if os.listdir(intrImgList) > 3
    #     intrImgList


class IntruderImg(models.Model):
    intruder_img = models.ImageField(max_length=100, blank=False, null=False, upload_to=get_image_path)
    intruder_label_id = models.CharField(max_length=100, null=False)
    romo_id = models.ForeignKey(ROMO, null=True, on_delete=models.CASCADE, related_name='+')
    uploaded_datetime = models.DateTimeField()
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return str(self.intruder_img)