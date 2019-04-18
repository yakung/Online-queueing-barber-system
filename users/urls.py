from django.urls import path
from . import views

urlpatterns = [
    # path('bloginr/', views.login_barber, name='blogin'),
    path('login/', views.login, name="login"),
    path("regb/", views.register_barber, name='regb')
]