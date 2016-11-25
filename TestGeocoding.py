# this is a test file for employing Geocoding module in python

import geocoder
g = geocoder.google('香港科學園')
print(g.latlng)
print(g.latlng[0])
print(g.latlng[1])