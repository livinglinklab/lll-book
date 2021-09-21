# lll-book

This module helps people extract grid related information from the living linklab database

![Grid of Link Lab](/img/lll_grid.png "lll_grid")

### What sensors do we have access to?

```python
import pickle
with open('book.pickle','rb') as f:
  df = pickle.load(f)
print(df)
'''
device_id location_general         type  ...                                             fields   name notes
0    018984f9          linklab          co2  ...  Concentration_ppm,H-Sensor,Humidity_%,T-Sensor...   CO-1   NaN
1    01939f0a          linklab          co2  ...  Concentration_ppm,H-Sensor,Humidity_%,T-Sensor...   CO-3   NaN
2    0506ed3a          linklab  light_level  ...  Illumination_lx,Range select,Supply voltage_V,...   LL-1   NaN
3    05060dd8          linklab  light_level  ...  Illumination_lx,Range select,Supply voltage_V,...   LL-2   NaN
4    050621a8          linklab  light_level  ...  Illumination_lx,Range select,Supply voltage_V,...   LL-6   NaN
..        ...              ...          ...  ...                                                ...    ...   ...
126  01834349          linklab      contact  ...                                       Contact,rssi  DS-25   NaN
127  01834351          linklab      contact  ...                                       Contact,rssi  DS-26   NaN
128  01834352          linklab      contact  ...                                       Contact,rssi  DS-27   NaN
129  01834365          linklab      contact  ...                                       Contact,rssi  DS-28   NaN
130  0183436c          linklab      contact  ...                                       Contact,rssi  DS-29   NaN

[120 rows x 8 columns]
'''
```

### How do I find which sensors are at the grid I'm interested in?

```python
import pickle

with open('grid-to-sensor.pickle','rb') as f:
  d = pickle.load(f)

d.keys()
# dict_keys([2, 6, 14, 18, 23, 24, 29, 35, 38, 40, 45, 51, 52, 70, 71, 74, 75, 77, 78, 89, 95, 97, 98, 101, 102, 103, 104, 105, 106, 107, 115, 117, 118, 120, 121, 122, 123, 132, 138, 140, 141, 147, 152, 158, 160, 162, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 178, 182, 183, 186, 192, 193, 196, 197])
# Hint: Not all grids have sensors in them

d[2]
'''
device_id location_general         type max_heartbeat_str     description  ...   name notes     x      y    z
29  0506d2cd          linklab  light_level             30min  6.51,29.29,3.1  ...  LL-36   NaN  6.51  29.29  3.1
'''
```

### How do I get data for that sensor for a specific time range?

```python
# def get_grid_df(grid_number, start_datetime, end_datetime):
#   # Returns a data frame of all the data points for sensors in that grid location
#   return grid_df

import utility as util
from datetime import datetime
s= datetime(2021,1,1) # start datetime
e= datetime(2021,9,20) # end datetime

fields = list(set(d[2]['fields'].values[0].split(',')))
# ['Illumination_lx', 'rssi', 'Supply voltage_V', 'Range select']
df = util.get_lfdf('Illumination_lx', s, e, list(d[2]['device_id']))

'''
time     0     1  ...         location_specific                 receiver value
0   2021-06-09 09:41:06-04:00  None  None  ...  North side of 201 Olsson  enocean-generic-gateway  64.0
1   2021-06-10 01:12:52-04:00  None  None  ...  North side of 201 Olsson  enocean-generic-gateway   0.0
2   2021-06-10 01:40:04-04:00  None  None  ...  North side of 201 Olsson  enocean-generic-gateway   0.0
3   2021-06-10 02:38:30-04:00  None  None  ...  North side of 201 Olsson  enocean-generic-gateway   0.0
4   2021-06-10 03:55:03-04:00  None  None  ...  North side of 201 Olsson  enocean-generic-gateway   0.0
..                        ...   ...   ...  ...                       ...                      ...   ...
643 2021-09-20 18:02:02-04:00  None  None  ...  North side of 201 Olsson                     None   0.0
644 2021-09-20 18:25:07-04:00  None  None  ...  North side of 201 Olsson                     None   0.0
645 2021-09-20 18:46:12-04:00  None  None  ...  North side of 201 Olsson                     None   0.0
646 2021-09-20 19:13:18-04:00  None  None  ...  North side of 201 Olsson                     None   0.0
647 2021-09-20 19:41:25-04:00  None  None  ...  North side of 201 Olsson                     None   0.0

[648 rows x 17 columns]
'''
```

### How can I plot values drawn from that sensor?

```python
import seaborn as sns # imports the seaborn module (https://seaborn.pydata.org/)
import matplotlib.pyplot as plt # imports the python data visualization library object (https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html)

sns.lineplot(x= 'datetime', y='value', data=df)
plt.title('Lux Value Over Time')
plt.show() # Shows the plot
```

![Light Plot](/img/example_plot.png "Example Plot")
