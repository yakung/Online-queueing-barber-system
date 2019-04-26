from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# Create your views here.
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
            print(flag)
            cus_profile = Customer.objects.get(user_id=req.user.id)
            style = cus_profile.style
            context['BarberShop_rec'] = BarberShop.objects.filter(style__contains=style)
            print(style)
            print(BarberShop.objects.filter(style__contains=style))
    context['BarberShop'] = BarberShop.objects.all()
    context['group'] = str(group)


    return render(req, 'core/index.html', context)


def detail(req, shop_id):
    print(BarberShop.objects.get(id=shop_id))
    context = {
        'BarberShop': BarberShop.objects.get(id=shop_id)
    }
    return render(req, 'core/detail.html', context)
