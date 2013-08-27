from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserInfo(User):
    date_of_birth = models.DateField()
    bio = models.TextField(blank=True)
    jabber = models.CharField(max_length=50, blank=True)
    skype = models.CharField(max_length=50, blank=True)
    other_contacts = models.TextField(blank=True)


class RequestInfo(models.Model):
    method = models.CharField(max_length=5)
    path = models.CharField(max_length=70)
    time = models.DateTimeField(auto_now_add=True)
