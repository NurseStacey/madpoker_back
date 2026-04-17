from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    email=models.EmailField(unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    image = models.ImageField(default='profile_pics/default.jpg',
                                     upload_to='profile_pics')
    phone = models.CharField(max_length=14)
    display_name = models.CharField(max_length=50, default='Mr. No Name')
    
    def __str__(self):
        return self.email