from matplotlib import pyplot as plt
import datetime
import json

# open the formatted and unformatted data
try:
    with open('/home/pratik/Projects/EQ map/data/formatted_data.json','r') as f:
        data = json.load(f)
    with open('/home/pratik/Projects/EQ map/data/raw_geojson.json','r') as fg:
        geojson_data = json.load(fg)
except:
    print('Could not find data json file. Make sure data is in proper format in formatted_data.json')
    raise SystemExit

magnitudes = [round(v['magnitude']) if v['magnitude'] is not None else 0 for v in data.values()]
times = [datetime.datetime.strptime(v['time'].split('+')[0],'%Y-%m-%d %H:%M:%S') for v in data.values()]

# plt.style.use('_mpl-gallery')

plt.hist(magnitudes)
plt.show()
