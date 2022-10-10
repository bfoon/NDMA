from django.shortcuts import render, redirect

# Create your views here.

def dashboard (request):
    # data display here
    return render(request, "dash/dash.html")

def disaster_map(request):
    # Map data by folium
    return render(request, "dash/map.html")