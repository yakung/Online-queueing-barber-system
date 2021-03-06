from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('blog/', views.blog, name="blog"),
    path('detail/<int:shop_id>', views.detail, name="detail"),
    path('review/<int:shop_id>/<int:h_id>', views.review, name='review')

]
