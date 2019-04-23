from django.contrib import admin
from django.contrib.auth.models import Permission


# Register your models here.
from .models import BarberShop, Customer

admin.site.register(Permission)
admin.site.register(BarberShop)
admin.site.register(Customer)
