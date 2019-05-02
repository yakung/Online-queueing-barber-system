from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import BarberShop, Customer
from .forms import RegisterBarberForm, RegisterCustomerForm, ChangePasswordForm, BarberShopForm, CustomerForm, LoginForm
from django.contrib.auth.models import Group


def _login(req):
    context = {}
    if req.method == 'POST':
        form = LoginForm(req.POST)
        context['form'] = form
        if form.is_valid():
            username = req.POST.get('username')
            password = req.POST.get('password')
            groupname = ""
            user = authenticate(req, username=username, password=password)
            if(user):
                groupname = user.groups.get()

            if user and str(groupname) == 'Customer':
                login(req, user)
                next_url = req.POST.get('next_url')  # hidden field input name
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('/')
            elif user and str(groupname) == 'BarberShop':
                login(req, user)
                next_url = req.POST.get('next_url')  # hidden field input name
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('/dashboard')
            else:
                context['error'] = 'Wrong username or password'
    next_url = req.GET.get('next')
    if next_url:
        print(next_url)
        context['next_url'] = next_url
    context['form'] = LoginForm()
    return render(req, 'users/login.html', context=context)

def _logout(req):
    logout(req)
    return redirect('login')

@login_required()
@permission_required('users.change_barbershop')
def update_barber(req):
    context = {}
    barbershop = BarberShop.objects.get(user_id=req.user.id)
    if req.method == "POST":
        form = BarberShopForm(req.POST, instance=barbershop)
        if form.is_valid():
            form.save()
            context['success'] = 'update successfully'

    else:
        form = BarberShopForm(instance=barbershop)

    context['form'] = form
    return render(req, 'users/update_barber.html', context)


def register_barber(req):
    if req.method == "POST":
        form = RegisterBarberForm(req.POST , req.FILES)
        if form.is_valid():
            if (not User.objects.filter(username=form.cleaned_data.get('username')).exists()):
                u = User.objects.create_user(username=form.cleaned_data.get('username'),
                                             email=form.cleaned_data.get('email'),
                                             password=form.cleaned_data.get('pass1'))
                bsg = Group.objects.get(name='BarberShop')
                bsg.user_set.add(u)
                BarberShop.objects.create(
                    user=u,
                    tel=form.cleaned_data.get('tel'),
                    address=form.cleaned_data.get('address'),
                    description=form.cleaned_data.get('description'),
                    shopname=form.cleaned_data.get('shopname'),
                    style=form.cleaned_data.get('style'),
                    pic=form.cleaned_data.get('pic')
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
                cs = Group.objects.get(name='Customer')
                cs.user_set.add(u)
                Customer.objects.create(
                    user=u,
                    tel=form.cleaned_data.get('tel'),
                    style=form.cleaned_data.get('style'),
                    gender=form.cleaned_data.get('gender'),
                    name=form.cleaned_data.get('name')

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

@login_required()
@permission_required('users.change_customer')
def update_customer(req):
    context = {}
    customer = Customer.objects.get(user_id=req.user.id)
    if req.method == "POST":
        form = CustomerForm(req.POST, instance=customer)
        if form.is_valid():
            form.save()
            context['success'] = 'update successfully'
    else:
        form = CustomerForm(instance=customer)

    context['form']=form
    return render(req, 'users/update_customer.html', context)


@login_required()
def changepass(req):
    if (req.method == "POST"):

        form = ChangePasswordForm(req.POST)
        if form.is_valid():
            user = req.user
            u = authenticate(req, username=user.username, password=form.cleaned_data.get('old_password'))
            if(u):
                u.set_password(form.cleaned_data.get('new_password1'))
                u.save()
                return redirect('login')
            else:
                form.add_error('old_password', "รหัสผ่านผิด")

    else:
        form = ChangePasswordForm()
    context = {
        'form': form
    }
    return render(req, 'users/change_password.html', context)


def choose(req):
    return render(req, 'users/choose.html')