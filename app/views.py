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

from app.forms import UserProfileForm, IPStackForm, HunterQueryForm
from app.models import UserProfile
from osint_tools import sockpuppet, ipstack, hunter
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
def shodan(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        if not query:
            return render(request, 'shodan.html', {'error': 'Please enter a query!'})

        url = f"https://api.shodan.io/shodan/host/search?key={SHODAN_API_KEY}&query={query}&facets=country"
        try:
            response = requests.get(url)
            print("Raw response:", response.text)
            data = response.json()
            return render(request, 'shodan.html', {'data': data, 'query': query})
        except requests.exceptions.RequestException as e:
            return render(request, "shodan.html", {"error": f"Chyba při komunikaci s API: {str(e)}"})
        except ValueError:
            return render(request, "shodan.html", {"error": f"Shodan API vrátilo neplatnou odpověď: {response.text}"})
    return render(request, 'shodan.html')

def sock_view(request):
    if request.method == 'GET':
        return render(request, "sock.html")
    if request.method == 'POST':
        # data = sockpuppet.generated_sock(request.user)
        data = sockpuppet.generated_sock()
        # request.session['sockpuppet'] = data
        return render(request, "sock.html", {"sockpuppet" : data})
    return None

def download_sock(request):
    sock_data = request.session.get('sockpuppet')
    if not sock_data:
        return JsonResponse({"error": "No sock data found."}, status=400)
    try:
        sock_json = json.dumps(sock_data, indent=4, ensure_ascii=False)
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

def hunter_view(request):
    if request.method == 'GET':
        form = HunterQueryForm()
        return render(request, "hunter.html", {"form": form})
    if request.method == 'POST':
        form = HunterQueryForm(request.POST)
        if form.is_valid():
            data = hunter.hunter(form.data['query'])
            return render(request, "hunter.html", {"hunter_data": data})

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
