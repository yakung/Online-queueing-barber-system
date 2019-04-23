from django.shortcuts import render
from django.contrib.auth.models import Group
# Create your views here.
from users.models import BarberShop


def index(req):
    return render(req,'core/index.html')