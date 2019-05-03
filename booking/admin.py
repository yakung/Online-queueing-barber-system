from django.contrib import admin
from django.contrib.auth.models import Permission


# Register your models here.
from .models import Queue

admin.site.register(Queue)