from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('disaster_map', views.disaster_map, name='disaster_map'),
    path('lit_map', views.lit_map, name='lit_map')
    ]