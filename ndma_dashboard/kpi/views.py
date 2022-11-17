from django.shortcuts import render
from django.db.models import Count, F, Value, Sum, Q, Count, Max, CASCADE, Min, FloatField, Avg, Func, CharField
from dash.models import map_data
from django.core.paginator import Paginator
# Create your views here.
# Create KPI heat map table
def kpi(request):
    # create and display data for the heat map table
    kpi_table = (map_data.objects.values('year','hazard','region','district').annotate(kpi_count=Count('hazard'), settle_count = Count('settlement'), max_id = Max('id')).order_by('-year','region', 'district','-kpi_count'))
    settle_list = map_data.objects.values('year','hazard','district','settlement').annotate(
        sett_count=Count('settlement')).order_by('-sett_count')
    # settle_list = Paginator(set1, per_page=10)

    context = {
        "kpi_table": kpi_table,
        "settle_list": settle_list,

    }
    return render(request, "kpi/kpi.html", context)
# def kpi_settlement(request, pk):
#     select_settle = map_data.objects.filter(id=pk)
#     settle_list = (map_data.objects.values('settlement').annotate(
#         sett_count=Count('settlement')))
#
#     context = {
#         "settle_list": settle_list,
#     }
#     return render(request, "kpi",context)

def kpi_list(request):

    context = {

    }
    return render(request, "kpi/kpi_list.html",context)

