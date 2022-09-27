import pandas as pd
from datetime import datetime
import utility as util
from statistics import mean
import csv

df = pd.read_csv("/Users/aparnak/Downloads/SAHB/lll-book/book_with_grids.csv",encoding= 'unicode_escape')

start = datetime(2022,7,15,0,0,0)
end = datetime(2022,9,10,0,0,0)
#awair = df[df["type"]=='awair_element']
#grid = list(set(awair['grid']))
#print(grid)

#with open('Example.csv', 'w', newline = '') as csvfile:
#    my_writer = csv.writer(csvfile, delimiter = ' ')
# for i in grid:
#     fields = list(set(df[df['grid']==i]['fields'].values[0].split(',')))
#     if 'co2' in fields:
#         for j in fields:
#             print(util.get_lfdf(j,start,end,list(df[df["grid"]==i]["device_id"])))
#     elif 'co2_ppm' in fields:
#         for j in fields:
#             util.get_lfdf(j,start,end,list(df[df["grid"]==i]["device_id"]))

readings = list(util.get_lfdf("co2_ppm",start,end,list(df[df["grid"]==4]["device_id"]))['value'])
print(readings)




