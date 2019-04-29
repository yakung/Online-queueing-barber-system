
from django.db import models

# Create your models here.
from django.utils.timesince import timeuntil

from users.models import BarberShop


class Blog(models.Model):
    BarberShop = models.ForeignKey(BarberShop, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    content = models.TextField(null=False)
    picture = models.ImageField(upload_to='feed_pic')
    create_date = models.DateTimeField()
    expired_date = models.DateTimeField()


