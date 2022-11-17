from django.shortcuts import render, redirect
import folium
import geocoder
from .models import map_data
import matplotlib.pyplot as plt
from folium import plugins
from django_pandas.io import read_frame
from django.db.models import Count, F, Value, Sum, Q, Count, Max, CASCADE, Min, FloatField, Avg, Func, CharField
import plotly.express as px

# Create your views here.

def dashboard (request):
    # data display here
    return render(request, "dash/dash.html")

def disaster_map(request):
    # get Gambia
    name = geocoder.osm('Gambia')
    # name2 = geocoder.osm('Banjul')
    # name3 = geocoder.osm('Bansang')
    data_map = map_data.objects.all()
    # Map data by folium
    data = data_map.values_list('lat', 'lon')
    map_ndam = folium.Map(location=data[0], zoom_start=8.5, control_scale=True)

    plugins.HeatMap(data).add_to(map_ndam)
    points1 = data

    # incidents_accident = folium.map.FeatureGroup()
    # car_group = folium.FeatureGroup(name="Car Accident").add_to(map)
    for lat_, lng_, label_ in data_map.all().values_list('lat', 'lon','hazard'):
        train_group = folium.map.FeatureGroup(name=label_).add_to(map_ndam)


        if label_ == 'Flashflood':
           train_group.add_child(folium.Marker(
                location=[lat_, lng_],
                popup=label_,
                icon=folium.Icon(color='red', icon='info-sign')
            )).add_to(map_ndam)
           # map.add_child(train_group)
        elif label_ == 'Windstorm':
            train_group.add_child(folium.Marker(
                location=[lat_, lng_],
                popup=label_,
                icon=folium.Icon(color='blue', icon='info-sign')
            )).add_to(map_ndam)
            # map.add_child(train_group)
        elif label_ == 'Domestic Fire':
            train_group.add_child(folium.Marker(
                location=[lat_, lng_],
                popup=label_,
                icon=folium.Icon(color='yellow', icon='info-sign')
            )).add_to(map_ndam)
            # map.add_child(train_group)
        else:
            train_group.add_child(folium.Marker(
                location=[lat_, lng_],
                popup=label_,
                icon=folium.Icon(color='green', icon='info-sign')
            )).add_to(map_ndam)


    # for tuple_ in points1:
    #     icon = folium.Icon(color='blue', icon="droplet-degree", icon_color="red", prefix='fa')
    # #     icon1 = folium.Icon(color='black', icon='car', icon_color="red", prefix='fa')
    #     train_group.add_child(folium.Marker(tuple_, icon=icon))
    # #     # car_group.add_child(folium.Marker(tuple_, icon=icon1))

    #
    # html = '''1st line<br>
    # 2nd line<br>
    # 3rd line'''
    #
    # iframe = folium.IFrame(html,
    #                        width=100,
    #                        height=100)
    #
    # popup = folium.Popup(iframe,
    #                      max_width=100)

    folium.LayerControl().add_to(map_ndam)

    # folium.Marker([name.lat, name.lng],
    #                        popup=popup).add_to(map)

    map_ndam = map_ndam._repr_html_()
    return render(request, "dash/map.html", {"map":map_ndam})

def kpi_chart(request):
    # Data for the chart
    kpi_table = map_data.objects.values_list('year','hazard').annotate(kpi_count = Count('hazard'))
    # df = read_frame(kpi_table)
    # counts_df = df
    # fig, ax = plt.subplots(1, 1)
    # fig.set_size_inches(20, 10)
    # counts_df.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    # plt.legend(loc='upper center', ncol=5, frameon=True, bbox_to_anchor=(0.5, 1.1), fancybox=True, shadow=True)
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # plt.xlabel('Year', size=15)
    # plt.ylabel('Number of Incidents', size=15)
    # plt.title('Crime in London (2020)', size=18, y=1.1)
    context = {
        "kpi_table":kpi_table

    }
    return render(request, "dash/kpi_chart.html", context)