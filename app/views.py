import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
import requests
import os

from django.urls import reverse
from django.views import View
from rest_framework import serializers

from app.forms import UserProfileForm, IPStackForm, FullhuntQueryForm, ReverseForm, ShodanForm
from app.models import UserProfile
from osint_tools import sockpuppet, ipstack, fullhunt, reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.serializers.json import DjangoJSONEncoder

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def sock_view(request):
    if request.method == 'GET':
        return render(request, "sock.html")
    if request.method == 'POST':
        # data = sockpuppet.generated_sock(request.user)
        data = sockpuppet.generated_sock()
        request.session['sockpuppet'] = data
        return render(request, "sock.html", {"sockpuppet" : data})
    return None

def download_sock(request):
    sock_data = request.session.get('sockpuppet')
    if not sock_data:
        return JsonResponse({"error": "No sock data found."}, status=400)
    try:
        sock_json = json.dumps(sock_data, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder)
        response = HttpResponse(sock_json, content_type='application/json')
        response["Content-Disposition"] = 'attachment; filename="sockpuppet.json"'
    except Exception as e:
        return JsonResponse({"error": f" Unexpected error: {str(e)}"}, status=500)
    return response

def ipstack_view(request):
    if request.method == 'GET':
        form = IPStackForm()
        return render(request, "ipstack.html", {"form": form})
    if request.method == 'POST':
        form = IPStackForm(request.POST)
        if form.is_valid():
            data = ipstack.ipstack(form.data['ip_address'])
            return render(request, "ipstack.html", {"ipstack_info": data})

def reverse_view(request):
    if request.method == 'GET':
        form = ReverseForm()
        return render(request, "reverse.html", {"form": form})
    if request.method == 'POST':
        form = ReverseForm(request.POST)
        if form.is_valid():
            data = reverse.reverse_image(form.data['img_url'])
            if data.get("image_results") and data.get("knowledge_graph"):
                return render(request, "reverse.html", {"rev_img": data["image_results"], "knowledge": data["knowledge_graph"]})
            elif data.get("image_results") and not data.get("knowledge_graph"):
                return render(request, "reverse.html",{"rev_img": data["image_results"]})
            else:
                return render(request, "reverse.html", {"error": data["error"]})

def fullhunt_view(request):
    if request.method == 'GET':
        form = FullhuntQueryForm()
        return render(request, "fullhunt.html", {"form": form})
    if request.method == 'POST':
        form = FullhuntQueryForm(request.POST)
        if form.is_valid():
            data = fullhunt.fullhunt(form.data['query'])
            return render(request, "fullhunt.html", {"fullhunt_data": data})

# @login_required
# def profile_view(request):
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect("profile")
#     else:
#         form = UserProfileForm(instance=profile)
#
#     return render(request, "profile.html", {"form": form})
