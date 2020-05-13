# -*- coding: utf-8 -*-

import folium
import geocoder

m = folium.Map(location=[48.8566, 2.3522])
g = geocoder.google('Mountain View, CA')
g.latlng
print(g)
m.save('index.html')
