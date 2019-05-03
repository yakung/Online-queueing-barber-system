
from django.db import models

# Create your models here.
from django.utils.timesince import timeuntil

from users.models import BarberShop, Customer


class Blog(models.Model):
    BarberShop = models.ForeignKey(BarberShop, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    content = models.TextField(null=False)
    picture = models.ImageField(upload_to='feed_pic')
    create_date = models.DateTimeField()
    expired_date = models.DateTimeField()

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    barbershop = models.ForeignKey(BarberShop, on_delete=models.CASCADE)
    description = models.TextField()
    score = (
        ('01', '1'),
        ('02', '2'),
        ('03', '3'),
        ('04', '4'),
        ('05', '5')
    )
    rating = models.CharField(choices=score, default='01', max_length=2)
    date = models.DateField(auto_now_add=True)





