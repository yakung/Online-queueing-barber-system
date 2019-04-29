from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
# Create your views here.
from booking.forms import QueueForm
from .models import Blog
from .forms import BlogForm
from users.models import BarberShop, Customer


def index(req):
    context = {}
    group = ""
    flag = ""
    if str(req.user) != "AnonymousUser":
        group = req.user.groups.get()
        try:
            flag = Customer.objects.get(user_id=req.user.id)
        except Customer.DoesNotExist:
            flag = Customer.objects.none()
        if flag:
            cus_profile = Customer.objects.get(user_id=req.user.id)
            style = cus_profile.style
            if(style):
                context['BarberShop_rec'] = BarberShop.objects.filter(style__contains=style)
    context['BarberShop'] = BarberShop.objects.all()
    context['group'] = str(group)


    return render(req, 'core/index.html', context)

def detail(req, shop_id):
    print(BarberShop.objects.get(id=shop_id))
    context = {
        'BarberShop': BarberShop.objects.get(id=shop_id),
    }
    return render(req, 'core/detail.html', context)

def is_barbershop(user):
    return user.groups.filter(name='BarberShop').exists()

@login_required()
@user_passes_test(is_barbershop)
def dashboard(req):
    user_id = req.user.id
    shop = BarberShop.objects.get(user_id=user_id)
    print(shop)
    if req.method == 'POST':
        form = BlogForm(req.POST, req.FILES)
        if form.is_valid():
            Blog.objects.create(
                BarberShop = shop,
                header = form.cleaned_data.get('header'),
                content=form.cleaned_data.get('content'),
                picture=form.cleaned_data.get('picture'),
                create_date=datetime.now(),
                expired_date=datetime.now() + timedelta(seconds=120)
            )
    else:
        form = BlogForm()
    context = {
        'blogform': form
    }
    return render(req, 'core/dashboard.html', context)

def feed(req):
    feeds = Blog.objects.all().order_by('-create_date')
    print(datetime.now())
    print(Blog.objects.filter(expired_date__lt=datetime.now()).exists())
    if(Blog.objects.filter(expired_date__lt=datetime.now()).exists()):
        Blog.objects.filter(expired_date__lt=datetime.now()).delete()
        print("delete success")

    context={
        'feeds': feeds,
    }
    return render(req, 'core/feed.html', context)