import json
import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

from django.urls import reverse

from app.forms import IPStackForm, FullhuntQueryForm, ReverseForm, ShodanSearchForm, ShodanHostForm, UnifiedForm
from osint_tools import sockpuppet, ipstack, fullhunt, reverse, shodan_api, dorking
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.serializers.json import DjangoJSONEncoder
import markdown

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
        data = sockpuppet.generate_sock()

        if data is False:
            status = "no_api"
            return render(request, "sock.html", {"sockpuppet": "None", "status": status})
        else:
            status = "success"

        request.session['sockpuppet'] = data
        data['work_bio'] = markdown.Markdown().convert(data['work_bio'])
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

def puppint_view(request):
    results = {}
    errors = []

    if request.method == 'POST':
        form = UnifiedForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.cleaned_data.get('service')
            ip = form.cleaned_data.get('host')
            image_url = form.cleaned_data.get('image_url')
            image_file = form.cleaned_data.get('image_file')
            query = form.cleaned_data.get('query')
            site = form.cleaned_data.get('site')
            filetype = form.cleaned_data.get('filetype')
            intitle = form.cleaned_data.get('intitle')
            intext = form.cleaned_data.get('intext')

            if form.cleaned_data.get('shodan'):
                try:
                    if ip:
                        results['shodan_host'] = shodan_api.shodan_host(ip)
                    else:
                        results['shodan_host'] = None

                    if service:
                        results['shodan_search'] = shodan_api.shodan_search(service)
                    else:
                        results['shodan_search'] = None
                except Exception as e:
                    errors.append(f"Shodan error: {str(e)}")
            else:
                results['shodan_search'] = None
                results['shodan_host'] = None


            try:
                if form.cleaned_data.get('ipstack') and ip:
                    results['ipstack'] = ipstack.ipstack(ip)
                else:
                    results['ipstack'] = None
            except Exception as e:
                errors.append(f"IPStack error: {str(e)}")


            try:
                if form.cleaned_data.get('fullhunt') and service:
                    results['fullhunt'] = fullhunt.fullhunt(service)
                else:
                    results['fullhunt'] = None
            except Exception as e:
                errors.append(f"FullHunt error: {str(e)}")

            try:
                if form.cleaned_data.get('reverse_image') and image_url:
                    results['reverse_image'] = reverse.reverse_image(image_url)
                else:
                    results['reverse_image'] = None
            except Exception as e:
                errors.append(f"Serpapi error: {str(e)}")

            try:
                if form.cleaned_data.get('dorking') and any([query, site, intitle, intext]):
                    dork = dorking.GoogleDork(query, site, filetype, intitle, intext)
                    results['google_dork'] = dork.google_dorking()
                else:
                    results['google_dork'] = None
            except Exception as e:
                errors.append(f"Serpapi error: {str(e)}")

            request.session['results'] = results

        return render(request, 'puppint.html', {'form': form, 'results': results, "errors": errors})
    else:
        form = UnifiedForm()
        return render(request, "puppint.html", {"form": form})

def download_results(request):
    data = request.session.get('results')
    if not data:
        return JsonResponse({"error": "No data found."}, status=400)
    try:
        data_json = json.dumps(data, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder)
        response = HttpResponse(data_json, content_type='application/json')
        response["Content-Disposition"] = 'attachment; filename="puppint_results.json"'
    except Exception as e:
        return JsonResponse({"error": f" Unexpected error: {str(e)}"}, status=500)
    return response
