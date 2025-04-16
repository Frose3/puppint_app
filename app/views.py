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

from app.forms import IPStackForm, FullhuntQueryForm, ReverseForm, ShodanSearchForm, ShodanHostForm
from osint_tools import sockpuppet, ipstack, fullhunt, reverse, shodan_api
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

        if data is False:
            status = "no_api"
            return render(request, "sock.html", {"sockpuppet": "None", "status": status})
        if data.get("code"):
            if data.code == 400:
                status = "invalid_api"
                return render(request, "sock.html", {"sockpuppet": data.message, "status": status})
            else:
                status = "error"
                return render(request, "sock.html", {"sockpuppet": data.message, "status": status})
        else:
            status = "success"

        request.session['sockpuppet'] = data
        return render(request, "sock.html", {"sockpuppet" : data, "status": status})
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
            data = ipstack.ipstack(form.cleaned_data['ip_address'])

            if data is False:
                status = "no_api"
                return render(request, "ipstack.html", {"ipstack_info": "None", "status": status})
            elif data == 2:
                status = "invalid_api"
                return render(request, "ipstack.html", {"ipstack_info": "None", "status": status})
            else:
                status = "success"
            return render(request, "ipstack.html", {"ipstack_info": data, "status": status})
        return None
    return None


def reverse_view(request):
    if request.method == 'GET':
        form = ReverseForm()
        return render(request, "reverse.html", {"form": form})
    if request.method == 'POST':
        form = ReverseForm(request.POST)
        if form.is_valid():
            data = reverse.reverse_image(form.cleaned_data['img_url'])

            if data is False:
                status = "no_api"
                return render(request, "reverse.html", {"rev_img": "None", "status": status})
            else:
                status = "success"

            if data.get("image_results") and data.get("knowledge_graph"):
                return render(request, "reverse.html", {"rev_img": data["image_results"], "knowledge": data["knowledge_graph"], "status": status})
            elif data.get("image_results") and not data.get("knowledge_graph"):
                return render(request, "reverse.html",{"rev_img": data["image_results"], "status": status})
            else:
                return render(request, "reverse.html", {"error": data['error'], "status": "error"})
        return None
    return None


def fullhunt_view(request):
    if request.method == 'GET':
        form = FullhuntQueryForm()
        return render(request, "fullhunt.html", {"form": form, "status":"invalid"})
    if request.method == 'POST':
        form = FullhuntQueryForm(request.POST)
        if form.is_valid():
            data = fullhunt.fullhunt(form.cleaned_data['query'])
            if data == 3:
                status = "no_credits"
                data = "no_credits"
            elif data == 2:
                status = "invalid_api"
                data = "invalid_api"
            elif data is False:
                status = "no_api"
                data = "no_api"
            else:
                status = "success"
            return render(request, "fullhunt.html", {"form": form, "fullhunt_data": data, "status": status})
        else:
            return render(request, "fullhunt.html", {"form": form, "status": "invalid"})
    return None

def shodan_view(request):
    if request.method == 'GET':
        form_host = ShodanHostForm()
        form_search = ShodanSearchForm()
        return render(request, "shodan.html", {"form_search": form_search, "form_host": form_host})
    if request.method == 'POST':
        if 'host' in request.POST:
            form_host = ShodanHostForm(request.POST)
            form_search = ShodanSearchForm()
            if form_host.is_valid():
                data = shodan_api.shodan_host(form_host.cleaned_data['host'])
                if data == 2:
                    status = "invalid_api"
                    data = "invalid_api"
                elif data is False:
                    status = "no_api"
                    data = "no_api"
                else:
                    status = "success"
                return render(request, "shodan.html", {"form_search": form_search, "form_host": form_host, "data": data, "status": status})
        elif 'service' in request.POST:
            form_host = ShodanHostForm()
            form_search = ShodanSearchForm(request.POST)
            print("POST:", request.POST)
            print("form_search errors:", form_search.errors)
            if form_search.is_valid():
                data = shodan_api.shodan_search(form_search.cleaned_data['service'])
                if data == 2:
                    status = "invalid_api"
                    data = "invalid_api"
                elif data is False:
                    status = "no_api"
                    data = "no_api"
                else:
                    status = "success"
                return render(request, "shodan.html", {"form_search": form_search, "form_host": form_host, "data": data, "status": status})
        else:
            status = "error"
            return render(request, "shodan.html", {"form_search": "None", "form_host": "None", "status": status})

    return None
