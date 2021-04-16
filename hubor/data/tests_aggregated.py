from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient
from data.models import *
from data.serializers import *
from accounts.models import *
from accounts.serializers import *
from api.test_util import *
import pandas as pd
import os

'''
client = APIClient()


print("=============")
print("Pandas ver. =", pd.__version__)
print("=============")
user = create_user(client, 0)
print("id =", str(user.id))
print("username =", user.username)
login(client, user)
df = pd.read_csv("./data/dummy_vs_data.csv")
df['time'] = pd.to_datetime(df['time'])

min_mean = df.groupby(pd.Grouper(key="time", freq="1min")).mean()
min_max = df.groupby(pd.Grouper(key="time", freq="1min")).max()
min_min = df.groupby(pd.Grouper(key="time", freq="1min")).min()
min_std = df.groupby(pd.Grouper(key="time", freq="1min")).std()
min_med = df.groupby(pd.Grouper(key="time", freq="1min")).median()
min_mean = min_mean.merge(min_max, left_on='time', right_on='time', suffixes=('_mean', '_max'))
min_mean = min_mean.merge(min_min, left_on='time', right_on='time', suffixes=('','_min'))
min_mean = min_mean.merge(min_std, left_on='time', right_on='time', suffixes=('','_std'))
min_mean = min_mean.merge(min_med, left_on='time', right_on='time', suffixes=('','_med'))

hr_mean = df.groupby(pd.Grouper(key="time", freq="1H")).mean()
hr_max = df.groupby(pd.Grouper(key="time", freq="1H")).max()
hr_min = df.groupby(pd.Grouper(key="time", freq="1H")).min()
hr_std = df.groupby(pd.Grouper(key="time", freq="1H")).std()
hr_med = df.groupby(pd.Grouper(key="time", freq="1H")).median()
hr_mean = hr_mean.merge(hr_max, left_on='time', right_on='time', suffixes=('_mean', '_max'))
hr_mean = hr_mean.merge(hr_min, left_on='time', right_on='time', suffixes=('',''))
hr_mean = hr_mean.merge(hr_std, left_on='time', right_on='time', suffixes=('','_std'))
hr_mean = hr_mean.merge(hr_med, left_on='time', right_on='time', suffixes=('','_med'))

day_mean = df.groupby(pd.Grouper(key="time", freq="1D")).mean()
day_max = df.groupby(pd.Grouper(key="time", freq="1D")).max()
day_min = df.groupby(pd.Grouper(key="time", freq="1D")).min()
day_std = df.groupby(pd.Grouper(key="time", freq="1D")).std()
day_med = df.groupby(pd.Grouper(key="time", freq="1D")).median()
day_mean = day_mean.merge(day_max, left_on='time', right_on='time', suffixes=('_mean', '_max'))
day_mean = day_mean.merge(day_min, left_on='time', right_on='time', suffixes=('',''))
day_mean = day_mean.merge(day_std, left_on='time', right_on='time', suffixes=('','_std'))
day_mean = day_mean.merge(day_med, left_on='time', right_on='time', suffixes=('','_med'))

month_mean = df.groupby(pd.Grouper(key="time", freq="1M")).mean()
month_max = df.groupby(pd.Grouper(key="time", freq="1M")).max()
month_min = df.groupby(pd.Grouper(key="time", freq="1M")).min()
month_std = df.groupby(pd.Grouper(key="time", freq="1M")).std()
month_med = df.groupby(pd.Grouper(key="time", freq="1M")).median()
month_mean = month_mean.merge(month_max, left_on='time', right_on='time', suffixes=('_mean', '_max'))
month_mean = month_mean.merge(month_min, left_on='time', right_on='time', suffixes=('',''))
month_mean = month_mean.merge(month_std, left_on='time', right_on='time', suffixes=('','_std'))
month_mean = month_mean.merge(month_med, left_on='time', right_on='time', suffixes=('','_med'))

counter = 0
means = [min_mean, hr_mean, day_mean, month_mean]
CHOICES = ['min',  'hr',  'day','month']

for i in range(len(means)):
    dfs = means[i]
    length = dfs.shape[0]
    for row in dfs.iterrows():
        counter += 1
        #print("%d out of %d"%(counter, length))
        
        payload = {
            'type': CHOICES[i],
            'time': str(row[0]) + "Z",
            'hr_mean': row[1]['hr_mean'],
            'hr_max': row[1]['hr_max'],
            'hr_min': row[1]['hr'],
            'hr_med': row[1]['hr_med'],
            'hr_std': row[1]['hr_std'],

            'rr_mean': row[1]['rr_mean'],
            'rr_max': row[1]['rr_max'],
            'rr_min': row[1]['rr'],
            'rr_med': row[1]['rr_med'],
            'rr_std': row[1]['rr_std'],
            
            'temp_mean': row[1]['temp_mean'],
            'temp_max': row[1]['temp_max'],
            'temp_min': row[1]['temp'],
            'temp_med': row[1]['temp_med'],
            'temp_std': row[1]['temp_std'],

            'spo2_mean': row[1]['spo2_mean'],
            'spo2_max': row[1]['spo2_max'],
            'spo2_min': row[1]['spo2'],
            'spo2_med': row[1]['spo2_med'],
            'spo2_std': row[1]['spo2_std'],
            
        }
        
        #print(payload)
        response = client.post('/api/aggregatedvs/%s/'%(str(user.id)), payload)
        assert response.status_code == 200, "Error!, expecting 200, get %d"%response.status_code
print("Total of %d tuples added!"%counter)


user = User.objects.get(username='testuser1')
login(client, user)
print(str(user.id))
request = '/api/vitalsign/%s/?from=2021-03-04 00:00:00Z&to=2021-03-31 00:00:00Z&type=min'%(str(user.id))
response = client.get(request)
print(len(response.data))
'''