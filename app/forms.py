from django import forms

class IPStackForm(forms.Form):
    ip_address = forms.CharField(max_length=15, label="IP adresa")
    class Meta:
        fields = ['ip_address']

class ReverseForm(forms.Form):
    img_url = forms.CharField(max_length=255, label="Reverse image")
    class Meta:
        fields = ['img_url']

class FullhuntQueryForm(forms.Form):
    query = forms.CharField(max_length=100, label="Hunter query")
    class Meta:
        fields = ['query']

class ShodanForm(forms.Form):
    service = forms.CharField(max_length=100, label="Service")
    class Meta:
        fields = ['service']