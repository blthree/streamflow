

import twitter
import json
import requests
from datetime import datetime

consumer_key = 'glhS6Kat7WwUBexZ2b56j09UG'
consumer_secret = 'bSbPTeqIXlOH4OxicSYArJ2rr0Sjfr6UAqbtXeETUCWUitWjfr'
access_token_key = '878427208259424256-iEGQ6sfqVhCFuawE3vroef0nIsSI8IH'
access_token_secret = 'Ul50jvPE5pNtX6cDEu7tNzAhaRtMAbu1BQQmmKqcEGC83'


api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)


site_num = '03226800'
base_url = 'https://waterservices.usgs.gov/nwis/iv/?format=json&sites=03226800&parameterCd=00060,00065&siteStatus=all'
r = requests.get(base_url)
parsed = json.loads(r.content)

flow = parsed['value']['timeSeries'][0]
depth = parsed['value']['timeSeries'][1]
site_name = flow['sourceInfo']['siteName']
flow_value = flow['values'][0]['value'][0]['value']
depth_value = depth['values'][0]['value'][0]['value']
# "2017-06-23T21:00:00.000-04:00"
last_updated = datetime.strptime(flow['values'][0]['value'][0]['dateTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')

str_flow = flow_value + ' cfs'
str_depth = depth_value + ' ft'
#print(site_name)
#print(str_flow, str_depth)
#print('Last updated: ' + str(last_updated) + ' EST')
full_str = site_name + '\n' + str_flow + '\n' + str_depth + '\n' + 'Last updated: ' + str(last_updated) + ' EST'
#print(len(full_str))
api.PostUpdate(full_str)
