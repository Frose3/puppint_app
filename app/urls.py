from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shodan/', views.shodan, name='shodan'),
    path('sockpuppet/', views.sock_view, name='sockpuppet'),
    path('download_sock', views.download_sock, name='download_sock'),
]