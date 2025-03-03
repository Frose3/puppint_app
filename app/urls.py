from django.urls import path
from app import views
from django.views.generic.base import TemplateView
from .views import SignUp

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('shodan/', views.shodan, name='shodan'),
    path('sockpuppet/', views.sock_view, name='sockpuppet'),
    path('sockpuppet/download', views.download_sock, name='download_sock'),
]