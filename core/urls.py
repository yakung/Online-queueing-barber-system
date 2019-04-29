from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('feed/', views.feed, name="feed"),
    path('detail/<int:shop_id>', views.detail, name="detail"),

]