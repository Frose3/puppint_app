from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gemini_api_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"API Keys for {self.user.username}"

class SockPuppet(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    date_of_birth = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    street_adress = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=255, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.name
