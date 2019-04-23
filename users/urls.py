from django.urls import path

from . import views
urlpatterns = [
    # path('bloginr/', views.login_barber, name='blogin'),
    path('login/', views._login, name="login"),
    path('logout/', views._logout, name="logout"),
    path("register-barber/", views.register_barber, name='regb'),
    path("register-customer/", views.register_customer, name='regc'),
    path("changepass/", views.changepass, name='changepass'),
    path("update-barbar/", views.update_barber, name='updateb'),
    path("update-customer/", views.update_customer, name='updatec'),
]
