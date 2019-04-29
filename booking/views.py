from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

# Create your views here.
from .forms import QueueForm

#check user group
def is_customer(user):
    return user.groups.filter(name='Customer').exists()

@login_required()
@user_passes_test(is_customer)
def reserve_queue(req, shop_id):
    if req.method == "POST":
        form_queue = QueueForm(req.POST)
        if form_queue.is_valid():
            print('pass2')
            pass
    else:
        form_queue = QueueForm()
    context = {
        'form_queue' : form_queue
    }
    return render(req, 'booking/queue.html', context)