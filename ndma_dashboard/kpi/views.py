from django.shortcuts import render

# Create your views here.
# Create KPI heat map table
def kpi(request):
    # create and display data for the heat map table
    return render(request, "kpi/kpi.html")