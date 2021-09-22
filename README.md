# lll-book

This module helps people extract grid related information from the living linklab database

![Grid of Link Lab](/img/lll_grid.png "lll_grid")

### What sensors do we have access to?

```python
import pandas as pd
df = pd.read_csv('book_with_grids.csv')
```

```python
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

### How do I find which sensors are at the grid I'm interested in? Let's say grid number 197?

```python
df[df['grid'] ==197]
```

device_id location_general         type max_heartbeat_str     description  ... notes      x     y    z  grid
117  050623c9          linklab  light_level             30min   54.18,1.6,3.1  ...   NaN  54.18  1.60  3.1   197
118  018a242d          linklab   temp_humid             15min  52.35,2.83,1.1  ...   NaN  52.35  2.83  1.1   197
119   1834365          linklab      contact             25min   52.35,3.0,1.1  ...   NaN  52.35  3.00  1.1   197


### How do I get data for that sensor for a specific time range?

```python
import utility as util
from datetime import datetime
s= datetime(2021,1,1) # start datetime
e= datetime(2021,9,20) # end datetime

fields = list(set(df[df['grid']==2]['fields'].values[0].split(',')))
# ['Illumination_lx', 'rssi', 'Supply voltage_V', 'Range select']
ldf = util.get_lfdf('Illumination_lx', s, e, list(df[df['grid']==2]['device_id']))
```
```python 
'''
time     0     1  ...         location_specific                 receiver value
0   2021-06-09 09:41:06-04:00  None  None  ...  North side of 201 Olsson  enocean-generic-gateway  64.0
1   2021-06-10 01:12:52-04:00  None  None  ...  North side of 201 Olsson  enocean-generic-gateway   0.0
2   2021-06-10 01:40:04-04:00  None  None  ...  North side of 201 Olsson  enocean-generic-gateway   0.0
3   2021-06-10 02:38:30-04:00  None  None  ...  North side of 201 Olsson  enocean-generic-gateway   0.0
4   2021-06-10 03:55:03-04:00  None  None  ...  North side of 201 Olsson  enocean-generic-gateway   0.0
..                        ...   ...   ...  ...                       ...                      ...   ...
637 2021-09-06 19:34:51-04:00  None  None  ...  North side of 201 Olsson                     None  80.0
638 2021-09-06 20:32:08-04:00  None  None  ...  North side of 201 Olsson                     None  80.0
639 2021-09-07 01:14:54-04:00  None  None  ...  North side of 201 Olsson                     None  80.0
640 2021-09-07 06:02:51-04:00  None  None  ...  North side of 201 Olsson                     None  80.0
641 2021-09-08 03:43:39-04:00  None  None  ...  North side of 201 Olsson                     None  80.0

[642 rows x 17 columns]
'''
```

### How can I plot values drawn from that sensor?

```python
import seaborn as sns # imports the seaborn module (https://seaborn.pydata.org/)
import matplotlib.pyplot as plt # imports the python data visualization library object (https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html)

sns.lineplot(x= 'time', y='value', data=ldf)
plt.title('Lux Value Over Time')
plt.show() # Shows the plot
```

![Light Plot](/img/example_plot.png "Example Plot")
