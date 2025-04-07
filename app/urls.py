from django.contrib.auth.views import LoginView
from django.urls import path
from app import views
from django.views.generic.base import TemplateView
from .views import SignUp

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('sockpuppet/', views.sock_view, name='sockpuppet'),
    path('sockpuppet/download', views.download_sock, name='download_sock'),
    # path('profile/', views.profile_view, name='profile'),
    path('ipstack/', views.ipstack_view, name='ipstack'),
    path('reverse/', views.reverse_view, name='reverse'),
    path('fullhunt/', views.fullhunt_view, name='fullhunt'),
]