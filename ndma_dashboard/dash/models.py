from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime
# User table
from django.forms import UUIDField
# Create your models here.
class map_data(models.Model):
    data_collector = models.CharField(max_length=10000, blank=True, null=True)
    hazard = models.CharField(max_length=10000, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    date_of_disaster = models.CharField(max_length=10000, blank=True, null=True)
    gender = models.CharField(max_length=10000, blank=True, null=True)
    age = models.CharField(max_length=10000, blank=True, null=True)
    region = models.CharField(max_length=10000, blank=True, null=True)
    district = models.CharField(max_length=10000, blank=True, null=True)
    ward = models.CharField(max_length=10000, blank=True, null=True)
    settlement = models.CharField(max_length=10000, blank=True, null=True)
    location = models.CharField(max_length=10000)
    lat = models.CharField(max_length=10000)
    lon = models.CharField(max_length=10000)
    alt = models.CharField(max_length=10000)
    geometry = models.CharField(max_length=10000, blank=True, null=True)

    def __str__(self):
        return f"{self.settlement}"