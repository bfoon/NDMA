from django.shortcuts import render, redirect
import folium
import geocoder
from .models import map_data
import matplotlib.pyplot as plt
from folium import plugins
from django_pandas.io import read_frame
from datetime import datetime
from django.db.models import Count, F, Value, Sum, Q, Count, Max, CASCADE, Min, FloatField, Avg, Func, CharField
import plotly.express as px
from plotly.offline import plot
import pandas as pd

# Create your views here.

def dashboard (request):
    # data display here
    return render(request, "dash/dash.html")

def disaster_map(request):
    # get Gambia
    name = geocoder.osm('Gambia')
    # name2 = geocoder.osm('Banjul')
    # name3 = geocoder.osm('Bansang')
    today = datetime.now()
    data_map = map_data.objects.all().filter( year=today.year)
    # Map data by folium
    data = data_map.values_list('lat', 'lon')
    map_ndam = folium.Map(location=data[0], zoom_start=8.5, control_scale=True)

    plugins.HeatMap(data).add_to(map_ndam)
    points1 = data

    # incidents_accident = folium.map.FeatureGroup()
    # car_group = folium.FeatureGroup(name="Car Accident").add_to(map)
    for lat_, lng_, label_, settle_ in data_map.all().values_list('lat', 'lon','hazard', 'settlement'):



        if label_ == 'Flashflood':
           train_group = folium.map.FeatureGroup(name=label_).add_to(map_ndam)
           train_group.add_child(folium.Marker(
                location=[lat_, lng_],
                popup=[label_, settle_],
                icon=folium.Icon(color='red', icon='info-sign')
            )).add_to(map_ndam)
           # map.add_child(train_group)
        elif label_ == 'Windstorm':
            train_group = folium.map.FeatureGroup(name=label_).add_to(map_ndam)
            train_group.add_child(folium.Marker(
                location=[lat_, lng_],
                popup=[label_, settle_],
                icon=folium.Icon(color='blue', icon='info-sign')
            )).add_to(map_ndam)
            # map.add_child(train_group)
        elif label_ == 'Domestic Fire':
            train_group = folium.map.FeatureGroup(name=label_).add_to(map_ndam)
            train_group.add_child(folium.Marker(
                location=[lat_, lng_],
                popup=[label_, settle_],
                icon=folium.Icon(color='cadetblue', icon='info-sign')
            )).add_to(map_ndam)
            # map.add_child(train_group)
        else:
            train_group = folium.map.FeatureGroup(name=label_).add_to(map_ndam)
            train_group.add_child(folium.Marker(
                location=[lat_, lng_],
                popup=[label_, settle_],
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

    maps_ndam = map_ndam._repr_html_()
    return render(request, "dash/map.html", {"map":maps_ndam})

def lit_map(request):
    # Data for the chart
    # kpi_table = map_data.objects.all()
    color_scale = [(0, 'orange'), (1, 'red')]
    temp = map_data.objects.all()
    mpdata = [
        {
        'lat': float(x.lat),
        'lon': float(x.lon),
        'settlement': x.settlement,
        'hazard': x.hazard
    } for x in temp
    ]
    df = pd.DataFrame(mpdata)
    fig = px.scatter_mapbox(df,
                            lat="lat",
                            lon="lon",
                            hover_name="settlement",
                            hover_data=['hazard'],
                            color="hazard",
                            color_continuous_scale=color_scale,
                            # size=df[["lat", "lon", "settlement","hazard"]].value_counts(),
                            zoom=8,
                            height=700
                            )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    gantt_plot = plot(fig, output_type="div")
    context = {
        "lit":gantt_plot

    }
    return render(request, "dash/lit_map.html", context)