from influxdb import InfluxDBClient
from decouple import config
import pickle
import logging
import os
from datetime import datetime, timedelta
import random
import utility as util
import arrow

''''
REFERENCES:
    https://www.influxdata.com/blog/getting-started-python-influxdb/
    https://influxdb-python.readthedocs.io/en/latest/examples.html
    https://github.com/influxdata/influxdb-python
'''


class Influx():
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.user = config('INFLUX_USER')
        self.password = config('INFLUX_PW')
        self.host = config('INFLUX_HOST')
        self.dbname = 'gateway-generic'  # 'linklab-users'
        self.port = 443
        self.ssl = True
        self.client = self.get_client()
        # self.local_data_storage = 'influx_data'

    def get_client(self, dbname='gateway-generic'):
        client = InfluxDBClient(host=self.host, port=self.port, username=self.user,
                                password=self.password, database=self.dbname, ssl=self.ssl)

        print('Retrieving client for: %s' % dbname)
        '''
        q_str = 'SELECT * FROM "lifeAssessment" WHERE (time >= now() - 16w)'
        result_set = client.query(q_str)
        logging.info(result_set)
        logging.info('Result set length: %s' % len(result_set))
        '''
        self.client = client
        return client

    def get_result_set(self, fieldname, add_param):  # show in new readme
        q_str = 'SELECT * FROM "%s" WHERE %s' % (fieldname, add_param)
        client = self.client
        result_set = client.query(q_str)
        return result_set

    def get_device_query_adds(self, device_id_list):
        q_append = ''
        count = 0
        for device_id in device_id_list:
            if count == 0:
                q_append += 'and ("device_id"=\'%s\'' % device_id
            else:
                q_append += 'or "device_id"=\'%s\'' % device_id
            count += 1
        q_append += ')'
        return q_append

    # python datetime objects
    def get_time_query_from_datetime(self, start_time, end_time):
        start_time = start_time.replace(microsecond=0)
        end_time = end_time.replace(microsecond=0)
        s = arrow.get(start_time).to('utc').datetime
        e = arrow.get(end_time).to('utc').datetime

        start_time = str(start_time).split('+')[0]
        end_time = str(end_time).split('+')[0]

        print('start_time: %s' % start_time)
        print('end_time: %s' % end_time)

        tq = "time >= '%s' and time < '%s'" % (start_time, end_time)
        # print(tq)
        return tq

    def create_pickle(self, fieldname='Temperature_°C', time_query='(time >= now()-1w)',  filename=None):
        client = self.client

        logging.info(client)
        logging.info(client.get_list_database())

        # logging.info(client.query('SHOW SERIES'))
        # logging.info('DATABASE switch: %s' %client.switch_database('gateway-generic'))
        logging.info('-' * 80)
        # q_str= 'SELECT mean("1") FROM "Temperature_°C" WHERE ("location_general" = "UVA")' # AND time >= now() - 24h GROUP BY time(1s), "device_id", "location_specific" fill(null)'

        # q_str= 'SELECT * FROM "gateway-generic"'
        # q_str= 'SHOW FIELD KEYS'
        # q_str = 'SELECT * FROM "%s" WHERE (time <= now())' % fieldname
        q_str = 'SELECT * FROM "%s" WHERE %s' % (fieldname, time_query)

        if filename == None:
            filename = '%s_%s' % (fieldname, time_query)
            filename = util.clean_file_name(filename) + '.pickle'

        # filename = os.path.join(self.local_data_storage, filename)

        if not os.path.isfile(filename):
            result_set = client.query(q_str)
            # logging.info(result_set)
            logging.info('Result set length: %s' % len(result_set))

            print('Saving file to: %s' % filename)
            with open(os.path.join(filename), 'wb') as f:
                pickle.dump(result_set, f)
        else:
            print('File found: %s' % filename)

        return self.read_result_set(filename)


if __name__ == '__main__':
    x = Influx()
    # x.get_client()
