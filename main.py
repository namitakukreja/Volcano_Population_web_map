import folium
import pandas
map = folium.Map(location= [38.58, -99.09], zoom_start = 6, tiles = "Stamen Terrain")
data = pandas.read_csv("Volcanoes.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_pick(elevation):
    if elevation <1000:
        return 'green'
    elif 1000 <=elevation <3000:
        return 'orange'
    else:
        return 'red'

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

fgv = folium.FeatureGroup(name="Volcanoes")
for lt, ln, el, name in zip(lat,lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    # print(html % (name, name, el))
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=9, popup=folium.Popup(iframe, parse_html="true"), fill_color=color_pick(el),color = "grey", fill_opacity = 0.7))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding="utf-8-sig").read(), style_function= lambda x : {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 < x['properties']['POP2005'] < 20000000 else 'red'}))
map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())
map.save('Map2.html')
