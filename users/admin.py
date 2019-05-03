from django.contrib import admin


# Register your models here.
from users.models import BarberShop, Customer

admin.site.register(BarberShop)
admin.site.register(Customer)