from django.urls import path

from booking import views

urlpatterns = [
    path('history/', views.history, name="history"),
]