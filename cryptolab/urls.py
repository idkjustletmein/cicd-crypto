"""URL configuration for CryptoLab project."""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Pages
    path('', views.index, name='index'),
    path('learn/', views.learn, name='learn'),
    path('about/', views.about, name='about'),
    path('security/', views.security, name='security'),
    
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # History
    path('history/', views.history_view, name='history'),
    
    # File upload
    path('upload-key/', views.upload_key_view, name='upload_key'),
    
    # API endpoints
    path('health/', views.health_check, name='health_check'),
    path('encrypt/', views.encrypt, name='encrypt'),
    path('decrypt/', views.decrypt, name='decrypt'),
    path('api/ciphers/', views.get_ciphers, name='get_ciphers'),
    path('api/history/', views.api_history, name='api_history'),
    path('api/history/delete/', views.api_delete_history, name='api_delete_history'),
    path('api/upload-key/', views.api_upload_key, name='api_upload_key'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
