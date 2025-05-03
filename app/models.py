from django.db import models
from django.contrib.auth.models import User

class SockPuppet(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    photo = models.ImageField(upload_to='sock_photos/', blank=True, null=True)
    date_of_birth = models.CharField(max_length=255, blank=True, null=True)
    birth_number = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    card_num = models.CharField(max_length=255, blank=True, null=True)
    card_cvv = models.CharField(max_length=255, blank=True, null=True)
    card_exp = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    work_bio = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
