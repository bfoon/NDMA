from django.db import models

# Create your models here.

class kpi_data(models.Model):

    hazard = models.CharField(max_length=1000, blank=True, null=True)
    kpi_code = models.CharField(max_length=1000, blank=True, null=True)
    kpi_color = models.CharField(max_length=1000, blank=True, null=True)
    kpi_desc = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hazard}"