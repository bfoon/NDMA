from django.db import models

# Create your models here.

class kpi_data(models.Model):

    hazard = models.CharField(max_length=1000, blank=True, null=True)
    kpi_code = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.hazard}"