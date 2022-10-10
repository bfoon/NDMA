from django.urls import path
from . import views

urlpatterns = [
    path('kpi', views.kpi, name='kip')
    ]