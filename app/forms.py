from django import forms

class IPStackForm(forms.Form):
    ip_address = forms.CharField(max_length=15, label="IP adresa")

class ReverseForm(forms.Form):
    img_url = forms.CharField(max_length=255, label="Reverse image")

class HunterQueryForm(forms.Form):
    query = forms.CharField(max_length=100, label="Hunter query")

class ShodanSearchForm(forms.Form):
    service = forms.CharField(max_length=100, label="Service")

class ShodanHostForm(forms.Form):
    host = forms.CharField(max_length=100, label="Host")

class UnifiedForm(forms.Form):
    service = forms.CharField(label="Doména", required=False)
    host = forms.GenericIPAddressField(label="IP adresa", required=False)
    image_url = forms.URLField(label="URL obrázku", required=False)
    query = forms.CharField(label="Query pro vyhledání", required=False)
    site = forms.CharField(label="Pro kterou stránku vyhledat", required=False)
    filetype = forms.CharField(label="Jaký typ souboru vyhledat", required=False)
    intitle = forms.CharField(label="Jaké query má být v názvu", required=False)
    intext = forms.CharField(label="Jaké query má být v textu", required=False)

    shodan = forms.BooleanField(label="Shodan", required=False)
    ipstack = forms.BooleanField(label="IPStack", required=False)
    hunter = forms.BooleanField(label="Hunter", required=False)
    reverse_image = forms.BooleanField(label="Reverse Image Search", required=False)
    dorking = forms.BooleanField(label="Dorking", required=False)