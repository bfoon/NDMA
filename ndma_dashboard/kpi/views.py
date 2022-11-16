from django.shortcuts import render
from django.db.models import Count, F, Value, Sum, Q, Count, Max, CASCADE, Min, FloatField, Avg, Func, CharField
from dash.models import map_data
# Create your views here.
# Create KPI heat map table
def kpi(request):
    # create and display data for the heat map table
    kpi_table = (map_data.objects.values('year','hazard','region','district').annotate(kpi_count=Count('hazard')).order_by('-year','region', 'district','-kpi_count'))
    context = {
        "kpi_table": kpi_table

    }
    return render(request, "kpi/kpi.html", context)
def kpi_list(request):

    context = {

    }
    return render(request, "kpi/kpi_list.html",context)

