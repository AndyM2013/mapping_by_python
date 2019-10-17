"""
This application is about using folium API to create a customized map.
In this applicaiton, there are three layers. The base layer is the world map.
the second layer is the vocano information in the United States
the last layer is about population differences

Install folium and pandas in terminal first
$pip3 install folium
$pip3 install pandas
"""

import folium
import pandas

# Declare a map object with coordinates, zoom size, and tile properties
# More folium methods could be found by typing help(map) in terminal
# The map object contain html, css and js for web server
map = folium.Map(location=[37.3382, -121.8863], zoom_start=5, tiles="Stamen Terrain")

data = pandas.read_csv("Volcanoes.txt") # Store all the data to a data object

latitudes = list(data["LAT"]) # Store all vocano latitudes in a list
longitudes = list(data["LON"]) # Store all vocano longitudes in a list
elevations = list(data["ELEV"]) # Store all vocano elevations in a list
names = list(data["NAME"]) # Store all vocano names in a list

# define a htmal tag
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
# Helper function for determining marker's color according to elevation
def markerColorProducer(elevation):
    if elevation < 1000:
        return 'green'
    elif elevation < 3000:
        return 'orange'
    else:
        return 'red'

# Declare a feature group varible to store vocano features
vocanoFeatureGroup = folium.FeatureGroup(name="Vocanoes")

# iterate latitude and longitude lists and assign them to feature group
for lt, ln, elv, name in zip(latitudes, longitudes, elevations, names):
    iframe = folium.IFrame(html=html % (name, name, elv), width=200, height=100)

    vocanoFeatureGroup.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color=markerColorProducer(elv))))

# Declare a feature group varible to store population features
populationFeatureGroup = folium.FeatureGroup(name="Population")

# Create data object from geojson file first and then
# run folium GeoJson() method to access the data
# add the results to feature group as a child
# change attributes by using lambda, x reprenents geo feature
# POP2005 represents population in 2005
populationFeatureGroup.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {
'fillColor': 'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
else 'red'
}))

# Add the feature groups object to map as a child
map.add_child(vocanoFeatureGroup)
map.add_child(populationFeatureGroup)

# Add layer control after map features have been setup
map.add_child(folium.LayerControl())

# Generate html file
map.save("UnitedStatesVocanoes.html")
