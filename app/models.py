from django.db import models
from django.contrib.auth.models import User

class SockPuppet(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    date_of_birth = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=255, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.name
