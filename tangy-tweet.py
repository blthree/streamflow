def lambda_handler(event, context):
    import twitter
    import json
    import requests
    from datetime import datetime

    consumer_key = ''
    consumer_secret = ''
    access_token_key = ''
    access_token_secret = ''

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
    # print(site_name)
    # print(str_flow, str_depth)
    # print('Last updated: ' + str(last_updated) + ' EST')
    full_str = site_name + '\n' + str_flow + '\n' + str_depth + '\n' + 'Last updated: ' + str(last_updated) + ' EST'
    # print(len(full_str))
    return api.PostUpdate(full_str)
