from django import forms

class IPStackForm(forms.Form):
    ip_address = forms.CharField(max_length=15, label="IP adresa")

class ReverseForm(forms.Form):
    img_url = forms.CharField(max_length=255, label="Reverse image")

class FullhuntQueryForm(forms.Form):
    query = forms.CharField(max_length=100, label="Hunter query")

class ShodanSearchForm(forms.Form):
    service = forms.CharField(max_length=100, label="Service")

class ShodanHostForm(forms.Form):
    host = forms.CharField(max_length=100, label="Host")