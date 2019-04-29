from django.db import models

# Create your models here.
from users.models import BarberShop, Customer


class Queue(models.Model):
    barbershop = models.ForeignKey(BarberShop, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    STATUS = (
        ('01', 'waiting'),
        ('02', 'processing'),
        ('03', 'finish')
    )
    status = models.CharField(max_length=1, default='01', choices=STATUS)
    start_queue = models.DateTimeField()
    end_queue = models.DateTimeField()
    ref_pic = models.ImageField(upload_to='ref_queue_pic', null=True)
    hairstyle = models.CharField(max_length=100, null=True)

    def __str__(self):
        return 'start(%s) - end(%s)' % (self.start_queue, self.end_queue)


