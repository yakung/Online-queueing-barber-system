from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class BarberShop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(null=False, max_length=10)
    address = models.TextField()
    shopname = models.CharField(null=False, max_length=250)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(null=False,max_length=10)
    style = models.CharField(null=False, max_length=100)
    MALE = "M"
    FEMALE = "F"
    OTHER = "X"
    GENDERS = (
        (MALE, 'ชาย'),
        (FEMALE, 'หญิง'),
        (OTHER, 'อื่น'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)