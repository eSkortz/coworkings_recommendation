from django.urls import path
from . import views

urlpatterns = [
    path('euclid/', views.MyView.euclid, name='euclid'),
    path('cluster/', views.MyView.cluster, name='cluster'),
    path('hamming/', views.MyView.hamming, name='hamming'),
    path('euclid_pro/', views.MyView.euclid_pro, name='euclid_pro'),
    path('get_coworkings/', views.MyView.get_coworkings, name='get_coworkings'),
]