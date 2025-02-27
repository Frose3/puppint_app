import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
import requests
import os

import osint_tools.sockpuppet
from osint_tools import sockpuppet

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
        data = sockpuppet.generated_sock()
        return render(request, "sock.html", {"sockpuppet" : data})
    return None

def download_sock(request):
    response = HttpResponse(json.dumps(sockpuppet, indent=4), content_type='application/json')
    response["Content-Disposition"] = 'attachment; filename="sockpuppet.json"'
    return response