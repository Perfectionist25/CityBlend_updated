from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.CloudinaryField(default='i.webp', null=True, blank=True)

    class Meta:
        db_table = 'users_profile'
