#-*- coding: utf-8 -*-
import folium
import pandas as pd
import branca.colormap as cm
import geopandas as gpd


def prefecture_photos():
    tokyo_data = pd.read_csv('prefecture_photo.csv', encoding='utf-8')
    tokyo_data['id'] = tokyo_data['id'].astype(str)
    geojson = r'new_prefecture.json'
    tokyo23_location = [35.658593, 139.745441]
    m = folium.Map(location=tokyo23_location, tiles='cartodbpositron', zoom_start=8)
    m.choropleth(geo_data=geojson,
                 name='choropleth',
                 data=tokyo_data,
                 columns=['id', 'count'],
                 key_on='feature.id',
                 fill_color='YlGnBu',
                 threshold_scale=[0, 5000, 10000, 30000, 50000, 100000, 300000],
                 nan_fill_color='red',
                 legend_name='Number of Photographs')

    folium.LayerControl().add_to(m)  # 增加圖層開關
    m.save(outfile="Prefecture.html")

def prefecture_clusters():
    #參考：https://vverde.github.io/blob/interactivechoropleth.html
    tokyo_data = pd.read_csv('prefecture_photo.csv', encoding='utf-8')
    tokyo_data['id'] = tokyo_data['id'].astype(str)
    nil=gpd.read_file('new_prefecture.json')
    tokyo_data = tokyo_data[['id', 'group']]
    nilpop = nil.merge(tokyo_data, on="id")
    x_map = nil.centroid.x.mean()
    y_map = nil.centroid.y.mean()
    mymap = folium.Map(location=[y_map, x_map], tiles='cartodbpositron', zoom_start=8)
    folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(mymap)
    colormap = cm.linear.YlGnBu_09.to_step(index=[0,1,2,3,4])
    colormap.caption = "Cluster"
    style_function = lambda x: {"weight": 0.7,
                                'color': 'black',
                                'fillColor': colormap(x['properties']['group']),
                                'fillOpacity': 0.75}
    NIL = folium.features.GeoJson(
        nilpop,
        style_function=style_function,
        control=False,
    )

    mymap.add_child(NIL)
    mymap.save(outfile="Japan_Prefecture_Cluster.html")

def Tokyo23_photos():
    tokyo_data = pd.read_csv('tokyo23data.csv', encoding='utf-8')
    tokyo_data['code'] = tokyo_data['code'].astype(str)
    geojson = r'new_tokyo23.json'
    tokyo23_location = [35.658593, 139.745441]
    m = folium.Map(location=tokyo23_location, tiles='cartodbpositron', zoom_start=12)
    m.choropleth(geo_data=geojson,
                 name='choropleth',
                 data=tokyo_data,
                 columns=['code', 'count'],
                 key_on='feature.id',
                 fill_color='YlGnBu',
                 threshold_scale=[0, 5000, 10000, 20000, 30000, 40000, 50000, 60000],
                 nan_fill_color='red',

                 legend_name='Number of Photographs')

    folium.LayerControl().add_to(m)
    m.save(outfile="Tokto23.html")
if __name__ == '__main__':
    prefecture_clusters()
    prefecture_photos()
    Tokyo23_photos()