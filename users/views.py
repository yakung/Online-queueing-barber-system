from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import BarberShop, Customer
from .forms import RegisterBarberForm, RegisterCustomerForm


def login(req):
    return render(req, 'users/login.html')


def register_barber(req):
    if req.method == "POST":
        form = RegisterBarberForm(req.POST)
        if form.is_valid():
            if (not User.objects.filter(username=form.cleaned_data.get('username')).exists()):
                u = User.objects.create_user(username=form.cleaned_data.get('username'),
                                             email=form.cleaned_data.get('email'),
                                             password=form.cleaned_data.get('pass1'))
                BarberShop.objects.create(
                    user=u,
                    tel=form.cleaned_data.get('tel'),
                    address=form.cleaned_data.get('address'),
                    shopname=form.cleaned_data.get('shopname')
                )
                return redirect('login')
            else:
                form.add_error('username', "Username นี้มีในระบบแล้ว")
    else:
        form = RegisterBarberForm()

    context = {
        'form': form
    }
    return render(req, 'users/register_barber.html', context)


def register_customer(req):
    if req.method == "POST":
        form = RegisterCustomerForm(req.POST)
        if form.is_valid():
            if (not User.objects.filter(username=form.cleaned_data.get('username')).exists()):
                u = User.objects.create_user(username=form.cleaned_data.get('username'),
                                             email=form.cleaned_data.get('email'),
                                             password=form.cleaned_data.get('pass1'))
                Customer.objects.create(
                    user=u,
                    tel=form.cleaned_data.get('tel'),
                    style=form.cleaned_data.get('style'),
                    gender=form.cleaned_data.get('gender')
                )
                return redirect('login')
            else:
                form.add_error('username', "Username นี้มีในระบบแล้ว")
    else:
        form = RegisterCustomerForm()

    context = {
        'form': form
    }
    return render(req, 'users/register_customer.html', context)
