from django.shortcuts import render, redirect
import folium
import geocoder
from folium import plugins

# Create your views here.

def dashboard (request):
    # data display here
    return render(request, "dash/dash.html")

def disaster_map(request):
    # get Gambia
    name = geocoder.osm('Gambia')
    name2 = geocoder.osm('Banjul')
    name3 = geocoder.osm('Bansang')
    # Map data by folium
    map = folium.Map(location=[name.lat, name.lng], zoom_start=8.5, control_scale=True)
    data = [[name.lat, name.lng, 3000],[name2.lat, name2.lng, 4999], [name3.lat, name3.lng, 4999]]
    plugins.HeatMap(data).add_to(map)
    points1 = [(name.lat, name.lng), (name2.lat, name2.lng), (name3.lat, name3.lng)]

    train_group = folium.FeatureGroup(name="Fire").add_to(map)
    car_group = folium.FeatureGroup(name="Car Accident").add_to(map)

    for tuple_ in points1:
        icon = folium.Icon(color='black', icon='fire', icon_color="red", prefix='fa')
        icon1 = folium.Icon(color='black', icon='car', icon_color="red", prefix='fa')
        train_group.add_child(folium.Marker(tuple_, icon=icon))
        car_group.add_child(folium.Marker(tuple_, icon=icon1))

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

    folium.LayerControl().add_to(map)
    # folium.Marker([name.lat, name.lng],
    #                        popup=popup).add_to(map)

    map = map._repr_html_()
    return render(request, "dash/map.html", {"map":map})

def kpi_chart(request):
    # Data for the chart

    context = {

    }
    return render(request, "dash/kpi_chart.html", context)