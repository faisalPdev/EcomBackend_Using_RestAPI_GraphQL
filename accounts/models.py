from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    username=models.CharField(unique=True,max_length=20)
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=10,blank=True,null=True,unique=True)
    address=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.username
