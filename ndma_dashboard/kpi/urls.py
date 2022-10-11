from django.urls import path
from . import views

urlpatterns = [
    path('kpi', views.kpi, name='kip'),
    path('kpi_list', views.kpi_list, name='kip_list'),

    ]