from django.urls import path
from app import views
from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('sockpuppet/', views.sock_view, name='sockpuppet'),
    path('sockpuppet/download', views.download_sock, name='download_sock'),
    path('puppint/', views.puppint_view, name='puppint'),
    path('puppint/download', views.download_results, name='download_results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)