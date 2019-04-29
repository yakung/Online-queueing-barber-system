from django.urls import path
from . import views
urlpatterns = [
    path('reserve/<int:shop_id>', views.reserve_queue, name="reserve")
]