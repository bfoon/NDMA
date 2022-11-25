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
# import plotly.graph_objects as go

# Create your views here.

def dashboard (request):
    # data display here
    dash = map_data.objects.all()
    kip_count =  dash.values('hazard').annotate(kcount = Count('hazard'))
    female = dash.filter(gender="Female")
    male = dash.filter(gender="Male")
    kpi = dash.values('hazard').annotate(kpi=Count("hazard"))
    district = dash.values('district').annotate(dist=Count("district"))
    region = dash.values('region').annotate(reg=Count("region"))
    context = {
        "dash" : dash,
        "kip_count" : kip_count,
        "male" : male,
        "kpi" : kpi,
        "district" : district,
        "region" : region,
        "female" : female
    }
    return render(request, "dash/dash.html", context)

def disaster_map(request):
    # get Gambia
    name = geocoder.osm('Gambia')
    # name2 = geocoder.osm('Banjul')
    # name3 = geocoder.osm('Bansang')
    today = datetime.now()
    data_map = map_data.objects.all().filter(year=today.year)
    # Map data by folium
    data = data_map.values_list('lat', 'lon')
    map_ndam = folium.Map(location=data[0], zoom_start=8.5, control_scale=True)

    plugins.HeatMap(data).add_to(map_ndam)
    # points1 = data
    # mpdata = [
    #     {
    #         'settlement': x.settlement,
    #         'hazard': x.hazard,
    #         'year': x.year
    #     } for x in data_map
    # ]
    # incidents_accident = folium.map.FeatureGroup()
    # car_group = folium.FeatureGroup(name="Car Accident").add_to(map)
    # for lat_, lng_, label_, settle_ in data_map.all().values_list('lat', 'lon','hazard', 'settlement'):
    #
    #
    #
    #     if label_ == 'Flashflood':
    #        train_group = folium.map.FeatureGroup(name=label_).add_to(map_ndam)
    #        train_group.add_child(folium.Marker(
    #             location=[lat_, lng_],
    #             popup=[label_,settle_],
    #             icon=folium.Icon(color='red', icon='info-sign')
    #         )).add_to(map_ndam)
    #        # map.add_child(train_group)
    #     elif label_ == 'Windstorm':
    #         train_group = folium.map.FeatureGroup(name=label_).add_to(map_ndam)
    #         train_group.add_child(folium.Marker(
    #             location=[lat_, lng_],
    #             popup=[label_,settle_],
    #             icon=folium.Icon(color='blue', icon='info-sign')
    #         )).add_to(map_ndam)
    #         # map.add_child(train_group)
    #     elif label_ == 'Domestic Fire':
    #         train_group = folium.map.FeatureGroup(name=label_).add_to(map_ndam)
    #         train_group.add_child(folium.Marker(
    #             location=[lat_, lng_],
    #             popup=[label_,settle_],
    #             icon=folium.Icon(color='cadetblue', icon='info-sign')
    #         )).add_to(map_ndam)
    #         # map.add_child(train_group)
    #     else:
    #         train_group = folium.map.FeatureGroup(name=label_).add_to(map_ndam)
    #         train_group.add_child(folium.Marker(
    #             location=[lat_, lng_],
    #             popup=[label_,settle_],
    #             icon=folium.Icon(color='green', icon='info-sign')
    #         )).add_to(map_ndam)


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

    # folium.Marker([data[0][0], data[0][1]]).add_to(map_ndam)

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
        'hazard': x.hazard,
        'year': x.year
    } for x in temp
    ]
    df = pd.DataFrame(mpdata)
    fig = px.scatter_mapbox(df,
                            lat="lat",
                            lon="lon",
                            hover_name="settlement",
                            hover_data=['hazard','year'],
                            color="hazard",
                            color_continuous_scale=color_scale,
                            # size=df[["lat", "lon", "settlement","hazard"]].value_counts(),
                            zoom=8,
                            height=700
                            )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_traces(marker={'size': 15}, selector=dict(mode="markers"))
    gantt_plot = plot(fig, output_type="div")
    context = {
        "lit":gantt_plot

    }
    return render(request, "dash/lit_map.html", context)

def kpi_charts(request):
    temp = (map_data.objects.annotate(gen_count = Count('gender'))).\
        values('gender', 'year','gen_count')

    df = pd.DataFrame(temp)
    fig = px.histogram(df, x='year', y='gen_count',
                       color='gender', barmode='group',
                       histfunc='count',
                       height=400)
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    # fig['layout']['yaxis'].update(autorange=True)
    bar_plot = plot(fig, output_type="div")

    temp1 = (map_data.objects.annotate(gen_count=Count('region'))). \
        values('region', 'year', 'gen_count', 'hazard')

    df1 = pd.DataFrame(temp1)
    fig1 = px.histogram(df1, x='year', y='gen_count',
                       color='region', barmode='group',
                       histfunc='count',
                       height=400)
    fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    # fig1['layout']['yaxis'].update(autorange=True)
    bar_plot1 = plot(fig1, output_type="div")

    temp2 = (map_data.objects.values('region', 'hazard').annotate(haz_count=Count('hazard')))

    df2 = pd.DataFrame(temp2)
    fig2 = px.bar(df2, x="region", y="haz_count", color="hazard", text_auto=True)
    fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    # fig2['layout']['yaxis'].update(autorange=True)
    bar_plot2 = plot(fig2, output_type="div")

    # df3 = px.data.gapminder()
    temp3 = map_data.objects.all()
    mpdata = [
        {
            'region': x.region,
            'hazard': x.hazard,
            'year': x.year
        } for x in temp3
    ]
    lst3 = pd.DataFrame(mpdata)
    df3 = lst3.groupby(["hazard","year"])["hazard"].size().reset_index(name="counts")
    df3 = df3.sort_values(by=['year'])
    # df3 = pd.DataFrame(mpdata)
    fig3 = px.bar(df3, x="year", y="counts", color="hazard", text_auto=True)
    fig3.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    # fig2['layout']['yaxis'].update(autorange=True)
    bar_plot3 = plot(fig3, output_type="div")
    # fig3.show()

    context = {
        'bar_plot':bar_plot,
        'bar_plot1':bar_plot1,
        'bar_plot2':bar_plot2,
        'bar_plot3':bar_plot3
    }
    return render(request, "dash/kpi_chart.html",context)