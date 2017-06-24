import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot

tangy = pd.read_csv('data/streamflow/olentangy-delaware.txt', comment='#', sep='\t')
tangy.drop(tangy[['agency_cd', '110322_00065_cd', '110323_00060_cd', '110322_00065', 'tz_cd']], axis=1, inplace=True)
tangy.columns = ['site_num', 'datetime', 'flow']
tangy.set_index(pd.to_datetime(tangy['datetime']), drop=True, inplace=True)
tangy.drop(['datetime'], axis=1, inplace=True)
tangy = tangy.resample('H').mean()

tangy_w = pd.read_csv('data/streamflow/olentangy-worthington.txt', comment='#', sep='\t')
tangy_w.drop(tangy_w[['agency_cd', '110324_00065_cd', '110325_00060_cd', '110324_00065', 'tz_cd']], axis=1, inplace=True)
tangy_w.columns = ['site_num', 'datetime', 'flow']
tangy_w.set_index(pd.to_datetime(tangy_w['datetime']), inplace=True)  # format='%Y-%m-%d %H:%M')
tangy_w.drop(['datetime'], axis=1, inplace=True)
tangy_w = tangy_w.resample('H').mean()


result = pd.DataFrame(pd.concat([tangy,tangy_w], join='inner'))
idx = result.index.date
idx2 = result.index.time
result.set_index([idx, idx2])


wo_only = result.flow[result['site_num'] == 3226800].astype('int')
del_only = result.flow[result['site_num'] == 3225500].astype('int')
new_tangy = pd.DataFrame()
new_tangy['delaware'] = del_only
new_tangy['worthington'] = wo_only
new_tangy.dropna(inplace=True)
print(new_tangy)
#new_tangy.plot.scatter(x='delaware', y='worthington')
#new_tangy.plot.hexbin(x='delaware', y='worthington')
new_tangy['2017-06-01':'2017-06-23'].plot()
plt.show()
a = autocorrelation_plot(new_tangy.worthington['2017-06-01':'2017-06-23'])
plt.show(a)
