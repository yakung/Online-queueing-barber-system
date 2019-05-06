from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

# Create your views here.
from pytz import timezone

from booking.models import Queue, History
from users.models import Customer

# check user group
def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['Customer', 'BarberShop']).exists()

def history(req):
    customer = Customer.objects.get(user_id=req.user.id)
    queues = Queue.objects.filter(customer_id=customer.id, status__in=['01', '02']).order_by('start_queue')
    queues_history = History.objects.filter(customer_id=customer.id).order_by('start_queue')
    History.objects.filter(start_queue__lt=timezone('Etc/GMT+7').localize(datetime.now())).delete()
    if req.method == 'POST':
        Queue.objects.get(id=req.POST.get('qid')).delete()
        messages.success(req, "ยกเลิกคิวสำเร็จ")
    context = {
        'queues' : queues,
        'queues_history': queues_history,
    }
    return render(req, 'booking/history.html', context)