from django import forms
from app.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gemini_api_key']
        widgets = {
            "gemeni_api_key": forms.TextInput(attrs={"class": "form-control", "placeholder": "Zadejte svůj Gemini API klíč"}),
        }