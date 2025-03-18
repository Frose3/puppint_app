from django import forms
from app.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gemini_api_key']
        widgets = {
            "gemini_api_key": forms.TextInput(attrs={"class": "form-control", "placeholder": "Zadejte svůj Gemini API klíč"}),
        }

class IPStackForm(forms.Form):
    ip_address = forms.CharField(max_length=15, label="IP adresa")
    class Meta:
        fields = ['ip_address']

class HunterQueryForm(forms.Form):
    query = forms.CharField(max_length=100, label="Hunter query")
    class Meta:
        fields = ['query']