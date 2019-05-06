from datetime import datetime, timedelta
import json
from django.db.models import Q, Avg
from django.db.models.functions import Round
from pytz import timezone
from dateutil.parser import parse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
# Create your views here.
from booking.models import Queue, History
from .models import Blog, Review
from .forms import BlogForm, ReviewForm
from users.models import BarberShop, Customer


def index(req):
    context = {}
    group = ""
    flag = ""
    shop = BarberShop.objects.all()
    if req.method == 'POST':
        search = req.POST.get('search')
        style = req.POST.get('style')
        rate = req.POST.get('rate')
        print(rate)
        shop = BarberShop.objects.all()
        if search != '':
            print(1)
            shop = BarberShop.objects.filter(Q(shopname__icontains=search) | Q(address__icontains=search))
            if style != '':
                print(2)
                shop = BarberShop.objects.filter((Q(shopname__icontains=search) | Q(address__icontains=search)),
                                                 Q(style__icontains=style))
        elif style != '':
            print(3)
            shop = BarberShop.objects.filter(Q(style__icontains=style))
            if search != '':
                print(4)
                shop = BarberShop.objects.filter((Q(shopname__icontains=search) | Q(address__icontains=search)),
                                                 Q(style__icontains=style))
        elif rate != '0' and rate:
            print(5)
            shop = BarberShop.objects.annotate(avg_rating=Round(Avg('review__rating'))).filter(avg_rating=rate)
        elif rate == '0' and rate:
            print(6)
            shop = BarberShop.objects.annotate(avg_rating=Round(Avg('review__rating'))).filter(avg_rating=None)

    # Get style
    if str(req.user) != "AnonymousUser":
        group = req.user.groups.filter(name__in=['BarberShop', 'Customer'])
        try:
            flag = Customer.objects.get(user_id=req.user.id)
        except Customer.DoesNotExist:
            flag = Customer.objects.none()
        if flag:
            cus_profile = Customer.objects.get(user_id=req.user.id)
            style = cus_profile.style
            if (style):
                context['style'] = style
    context['BarberShop'] = shop
    context['group'] = str(group)

    return render(req, 'core/index.html', context)


def detail(req, shop_id):
    q = Queue.objects.filter(barbershop_id=shop_id)
    review = Review.objects.filter(barbershop_id=shop_id).order_by('-date')[0:3]
    blogs = Blog.objects.filter(BarberShop_id=shop_id).order_by('-create_date')[0:2]
    queues = []
    success=None
    for i in q:
        print(i)
        queue = {
            'start_date': i.start_queue,
            'end_date': i.end_queue
        }
        queues.append(queue)
    if req.method == 'POST':
        if req.user.groups.filter(name='Customer').exists():
            Queue.objects.create(
                barbershop=BarberShop.objects.get(id=shop_id),
                customer=Customer.objects.get(user_id=req.user.id),
                start_queue=parse(req.POST.get('start_queue')),
                end_queue=parse(req.POST.get('end_queue')),
                ref_pic=req.FILES.get('pic'),
                hairstyle=req.POST.get('hairstyle')
            )
            success = 'จองคิวสำเร็จ'
            return redirect('history')
        else:
            messages.error(req, 'Please sign in as customer!')
            return redirect('login')
    context = {
        'BarberShop': BarberShop.objects.get(id=shop_id),
        'queue': json.dumps(queues, indent=4, sort_keys=True, default=str),
        'review':review,
        'blogs':blogs,
        'success':success
    }
    return render(req, 'core/detail.html', context)


def is_barbershop(user):
    return user.groups.filter(name='BarberShop').exists()


@login_required()
@user_passes_test(is_barbershop)
def dashboard(req):
    context = {}
    user_id = req.user.id
    shop = BarberShop.objects.get(user_id=user_id)
    print(shop)
    if req.method == 'POST':
        form = BlogForm(req.POST, req.FILES)
        status = req.POST.get('status')
        print(status)
        update = None
        if (status):
            if (status == '03'):
                q = Queue.objects.get(id=req.POST.get('qid'))
                h = History.objects.get_or_create(
                    customer=q.customer,
                    barbershop=q.barbershop,
                    start_queue=q.start_queue,
                    end_queue=q.end_queue,
                    status='03'
                )
                update = Queue.objects.filter(id=req.POST.get('qid')).update(
                    status=status)
            elif status == '04':
                q = Queue.objects.get(id=req.POST.get('qid'))
                h = History.objects.get_or_create(
                    customer=q.customer,
                    barbershop=q.barbershop,
                    start_queue=q.start_queue,
                    end_queue=q.end_queue,
                    status='04'
                )
                messages.error(req, "คิวของคุณถูกยกเลิก")
                q.delete()
                print('delete q 04')
            else:
                update = Queue.objects.filter(id=req.POST.get('qid')).update(
                    status=status
                )
            if (update):
                context['success'] = 'อัพเดทสถานะสำเร็จ'
        else:
            context['error'] = 'โปรดเลือกสถานะ'
        if form.is_valid():
            Blog.objects.create(
                BarberShop=shop,
                header=form.cleaned_data.get('header'),
                content=form.cleaned_data.get('content'),
                picture=form.cleaned_data.get('picture'),
                create_date=timezone('Etc/GMT+7').localize(datetime.now()),
                expired_date=timezone('Etc/GMT+7').localize(datetime.now() + timedelta(days=14))
            )
            context['success'] = 'โปรโมทสำเร็จ'
    else:
        form = BlogForm()
    context['queues'] = Queue.objects.filter(barbershop_id=shop.id).order_by('start_queue')
    context['blogform'] = form
    return render(req, 'core/dashboard.html', context)


def blog(req):
    feeds = Blog.objects.all().order_by('-create_date')
    print(datetime.now())
    print(Blog.objects.filter(expired_date__lt=timezone('Etc/GMT+7').localize(datetime.now())).exists())
    if (Blog.objects.filter(expired_date__lt=timezone('Etc/GMT+7').localize(datetime.now())).exists()):
        Blog.objects.filter(expired_date__lt=timezone('Etc/GMT+7').localize(datetime.now())).delete()
        print("delete success")

    context = {
        'feeds': feeds,
    }
    return render(req, 'core/feed.html', context)


def is_customer(user):
    return user.groups.filter(name='Customer').exists()


@login_required()
@user_passes_test(is_customer)
def review(req, shop_id, h_id):
    context = {}
    shop = BarberShop.objects.get(id=shop_id)
    customer = Customer.objects.get(user_id=req.user.id)

    if req.method == 'POST':
        form = ReviewForm(req.POST)
        if form.is_valid():
            Review.objects.create(
                barbershop=shop,
                customer=customer,
                description=form.cleaned_data.get('description'),
                rating=int(req.POST.get('rating'))
            )

            History.objects.filter(id=h_id).update(
                status='05'
            )
            messages.success(req, 'รีวิวร้านสำเร็จ')
            return redirect('history')
    else:
        form = ReviewForm()
    context['form'] = form
    context['shop'] = shop
    return render(req, 'core/review.html', context)
