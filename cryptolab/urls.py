"""URL configuration for CryptoLab project."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('learn/', views.learn, name='learn'),
    path('about/', views.about, name='about'),
    path('security/', views.security, name='security'),
    path('encrypt/', views.encrypt, name='encrypt'),
    path('decrypt/', views.decrypt, name='decrypt'),
    path('api/ciphers/', views.get_ciphers, name='get_ciphers'),
]


