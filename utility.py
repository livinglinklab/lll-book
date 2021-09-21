import re
import os
import pickle
import json
import pandas as pd
from datetime import datetime, timedelta
import pprint
import influxdb_interface as inf
# import bookkeeper as bk
from tqdm import tqdm
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import collections
import hashlib
from slugify import slugify
import math
from collections import Counter
from dateutil import tz
import arrow


def save_pickle(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

    print('[%s] File written: %s' % (os.path.isfile(filename), filename))


def load_pickle(filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)


def get_location(df, id):
    if id in df['device_id'].values:
        cell = df[df['device_id'] == id]['description'].values[0]
        if not pd.isnull(cell):
            return [float(v) for v in cell.split(',')]
    return None


def convert_influx_time_to_datetime(time_str, timezone):
    # print(time_str)
    # return datetime.strptime(time_str[:19], '%Y-%m-%dT%H:%M:%S')
    t = arrow.Arrow.strptime(time_str[:19], '%Y-%m-%dT%H:%M:%S')
    return t.to(timezone).datetime  # utc.to('local').datetime


def convert_result_set_to_dict(result_set, rs_field='value'):
    d = {}
    print('result set keys: %s' % result_set.keys())
    if (len(result_set.keys()) > 0):
        field_name = list(result_set.keys())[0][0]  # not always true?

        for point in result_set.get_points(field_name):
            dt = convert_influx_time_to_datetime(point['time'])
            # print(dt, end='\r')

            device_id = point['device_id']
            val = point[rs_field]

            if not device_id in d:
                d[device_id] = []

            d[device_id].append({'time': dt, 'value': val})
    result_dict = d
    return result_dict


def get_rs_from_influx(fieldname, start_time, end_time, device_ids=None):
    '''
    return device on left, timeframe on top
    '''
    x = inf.Influx()
    a = x.get_time_query_from_datetime(start_time, end_time)

    if device_ids is not None:
        a += x.get_device_query_adds(device_ids)

    r = x.get_result_set(fieldname, a)

    return r


def get_cache_filename(fieldname, start_time, end_time, device_ids=None, append=None, file_ext='.pickle'):
    if device_ids != None:
        devices_hash = hashlib.md5(('%s' % device_ids).encode()).hexdigest()
    else:
        devices_hash = None

    str = '99_%s%s%s%s' % (fieldname, start_time, end_time, devices_hash)
    if append is None:
        return 'cache/' + slugify(str) + file_ext
    else:
        return 'cache/' + slugify(str + '_%s' % append) + file_ext


def get_cache_rs(fieldname, start_time, end_time, device_ids=None):
    filename = get_cache_filename(fieldname, start_time, end_time, device_ids)

    if os.path.isfile(filename):
        print('File loaded: %s ' % filename)
        return load_pickle(filename)
    else:
        print('File not found at : %s' % filename)
        rs = get_rs_from_influx(fieldname, start_time, end_time, device_ids)
        save_pickle(rs, filename)
        return rs


def get_longform_df(result_set, timezone='US/Eastern'):
    # essentially converting the result set to long_form
    df = pd.DataFrame([pt for pt in result_set.get_points()])
    # print('-' * 80)
    # print(df)

    # convert the string time to datetime objects
    if 'time' in df.columns:
        df['time'] = df['time'].map(
            lambda x: convert_influx_time_to_datetime(x, timezone))
        return df
    else:
        return None


def get_lfdf(fieldname, start_time, end_time, device_ids=None, timezone='US/Eastern'):
    return get_longform_df(get_rs_from_influx(fieldname, start_time, end_time, device_ids=device_ids), timezone)


def get_cache_lfdf(fieldname, start_time, end_time, device_ids=None):
    filename = get_cache_filename(
        fieldname, start_time, end_time, device_ids=device_ids)

    if os.path.isfile(filename):
        print('File loaded: %s ' % filename)
        return load_pickle(filename)
    else:
        df = get_lfdf(fieldname, start_time, end_time, device_ids)
        save_pickle(df, filename)
        return df


# assumes you didn't mess up the field name
def get_cache_health_score(pdf, s, e, freq_str, fieldname):
    filename = get_cache_filename(
        fieldname, s, e, list(pdf['device_id']), freq_str)

    if os.path.isfile(filename):
        print('File loaded: %s ' % filename)
        return load_pickle(filename)
    else:
        score = get_health_score(pdf, s, e, freq_str)
        save_pickle(score, filename)
        return score


def main():
    with open('book.pickle', 'rb') as f:
        ddf = pickle.load(f)
    s = datetime(2021, 8, 1)
    e = datetime(2021, 9, 1)

    devices = list(ddf[ddf['type'] == 'light_level']['device_id'])
    devices.sort()  # that way you get the same order
    rs = get_cache_rs('Illumination_lx', s, e, devices)
    return get_longform_df(rs)


if __name__ == '__main__':
    df = main()
    print(df)
