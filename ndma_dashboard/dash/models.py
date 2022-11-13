from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime
# User table
from django.forms import UUIDField
# Create your models here.
class map_data(models.Model):
    lon = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    alt = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True, null=True)
    ward = models.CharField(max_length=100, blank=True, null=True)
    settlement = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    geometry = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.settlement}"