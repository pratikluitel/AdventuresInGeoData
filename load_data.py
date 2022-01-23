import requests
import datetime
import json

data = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?\
    format=geojson&minlatitude=20&maxlatitude=35&minlongitude=75&maxlongitude=95&starttime=100-01-01').json()

formatted_data = {}

for feature in data['features']:
    id, properties, geometry = feature['id'], feature['properties'], feature['geometry']
    country = properties['place'].split(',')[-1].strip()

    if country == 'Nepal':
        formatted_data[id] = {
            'magnitude': properties['mag'],
            'place': properties['place'],
            'time': datetime.datetime.fromtimestamp(int(properties['time']/1000), tz=datetime.timezone.utc),
            'coordinates':geometry['coordinates'][:2]
        }

with open('raw_geojson.json','w') as f:
    json.dump(data, f, indent=3, default=str)