from matplotlib import pyplot as plt
import datetime
import json

try:
    with open('formatted_data.json','r') as f:
        data = json.load(f)
except:
    print('Could not find data json file. Make sure data is in proper format in formatted_data.json')

magnitudes = [round(v['magnitude']) if v['magnitude'] is not None else 0 for v in data.values()]
times = [datetime.datetime.strptime(v['time'].split('+')[0],'%Y-%m-%d %H:%M:%S') for v in data.values()]

# plt.style.use('_mpl-gallery')

plt.scatter(times, magnitudes)
plt.show()
