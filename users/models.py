from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Avg, Count
from django.db.models.functions import Round


class BarberShop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(null=False, max_length=10)
    address = models.TextField()
    shopname = models.CharField(null=False, max_length=250)
    style = models.CharField(null=False, max_length=100)
    description = models.TextField()
    pic = models.ImageField(upload_to='shop_pic', default='shop_pic/default.jpg')

    def get_review(self):
        return self.review_set.all()
    def get_review_count(self):
        return self.review_set.aggregate(amount_review = Count('id'))
    def get_review_score(self):
        return self.review_set.aggregate(avg_rating = Round(Avg('rating')))
    def __str__(self):
        return self.shopname

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=100)
    tel = models.CharField(null=False, max_length=10)
    style = models.CharField(null=True, max_length=100)
    MALE = "M"
    FEMALE = "F"
    OTHER = "X"
    GENDERS = (
        (MALE, 'ชาย'),
        (FEMALE, 'หญิง'),
        (OTHER, 'อื่น'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)
    def __str__(self):
        return self.name