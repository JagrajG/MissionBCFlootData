import geopandas as gpd
import folium
from branca.element import Template, MacroElement

watercourses = gpd.read_file("data/watercourses/Watercourses.shp")
watercourses = watercourses.to_crs(epsg=4326)

watercourses_m = watercourses.to_crs(epsg=26910)
buffered = watercourses_m.copy()
buffered["geometry"] = buffered.buffer(30)
buffered = buffered.to_crs(epsg=4326)

m = folium.Map(location=[49.13, -122.3], zoom_start=12)

water_layer = folium.FeatureGroup(name="Watercourses", show=True)
folium.GeoJson(
    watercourses,
    style_function=lambda x: {"color": "blue"},
).add_to(water_layer)
water_layer.add_to(m)

buffer_layer = folium.FeatureGroup(name="Flood Risk Buffer (30m)", show=True)
folium.GeoJson(
    buffered,
    style_function=lambda x: {"color": "red", "fillColor": "red", "fillOpacity": 0.3},
).add_to(buffer_layer)
buffer_layer.add_to(m)

folium.LayerControl().add_to(m)

legend_html = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed; 
    bottom: 50px;
    left: 50px;
    width: 200px;
    background-color: white;
    border:2px solid grey;
    z-index:9999;
    font-size:14px;
    padding: 10px;
    ">
    <b>Legend</b><br>
    <span style="background-color:red;opacity:0.7;width:12px;height:12px;display:inline-block;"></span>
    Flood Buffer (30m)<br>
    <span style="background-color:blue;opacity:0.7;width:12px;height:12px;display:inline-block;"></span>
    Watercourses
</div>
{% endmacro %}
"""
legend = MacroElement()
legend._template = Template(legend_html)
m.get_root().add_child(legend)

m.save("mission_flood_buffer_map.html")
print("Final map saved with legend and toggle: mission_flood_buffer_map.html")
