#!/usr/bin/python
import numpy
import csv
import datetime
import matplotlib
import json

## read in weather.json
## schema described below:
"""
[
  {'response':{JUNK}
  'history':{'date':{hour, mday, min, mon, pretty, tzname, year}
    utcdate: {similar to date but with diff timezones}
    observations:[
      {
      [u'heatindexm',
      u'windchillm',
      u'wdire',
      u'wdird',
      u'windchilli',
      u'hail',
      u'heatindexi',
      u'precipi',
      u'thunder',
      u'pressurei',
      u'snow',
      u'pressurem',
      u'fog',
      u'icon',
      u'precipm',
      u'conds',
      u'tornado',
      u'hum',
      u'tempi',
      u'tempm',
      u'dewptm',
      u'rain',
      u'dewpti',
      u'date',
      u'visi',
      u'vism',
      u'utcdate',
      u'wgusti',
      u'metar',
      u'wgustm',
      u'wspdi',
      u'wspdm']
      }, ...
    ]
    dailysummary:{
      
    }
  }


"""


## output a csv with one line per hour, with timestamp

weather_raw = json.load(open('data_original/wunderground.json','r'))

## days since jesus
#datetime.datetime.strptime('2012-05-02','%Y-%m-%d').date().toordinal()

ignored_keys = [u'utcdate', u'metar']
non_numerical_keys=[u'icon', u'conds', u'wdire']
numerical_keys = [u'heatindexm', u'windchillm', u'wdird', u'windchilli', u'hail', u'heatindexi', u'precipi', u'thunder', u'pressurei', u'snow', u'pressurem', u'fog', u'precipm', u'tornado', u'hum', u'tempi', u'tempm', u'dewptm', u'rain', u'dewpti', u'visi', u'vism', u'wgusti', u'wgustm', u'wspdi', u'wspdm']

## for reference
zeroAD = datetime.datetime(01,01,01)

## first count the number of rows
n = 0
for day in weather_raw:
    for obs in day['history']['observations']:
        n += 1
cols = len(non_numerical_keys + numerical_keys + ignored_keys) + 2

## preallocate the python array
weather = numpy.zeros((n,cols), dtype=object)

## iterate over day
n = 0
for day in weather_raw:
    ## iterate over observation
    for obs in day['history']['observations']:
        labels = []
        ## handle the date
        timestamp_raw = obs['date']
        timestamp = datetime.datetime(int(timestamp_raw['year']), int(timestamp_raw['mon']), int(timestamp_raw['mday']), int(timestamp_raw['hour']), int(timestamp_raw['min']))
        ## add the date, hour and minute as standalone values
        weather[n,len(labels)] = str(timestamp.date())
        labels.append('date')
        ## hour
        weather[n,len(labels)] = str(timestamp.hour)
        labels.append('hour')
        ## min
        weather[n,len(labels)] = str(timestamp.minute)
        labels.append('min')
        ## calculate the number of minutes since 0AD in eastern daylight time
        tdiff_since_0AD = (timestamp - zeroAD)
        mins_since_0AD = tdiff_since_0AD.total_seconds() / 60.0
        weather[n,len(labels)] = mins_since_0AD
        labels.append('mins_since_0AD_edt')
        ## handle all non-numerical fields
        for key in non_numerical_keys:
            weather[n,len(labels)] = obs[key].lower()
            labels.append(key)
        for key in numerical_keys:
            weather[n,len(labels)] = float(obs[key])
            labels.append(key)
        n += 1

## get labels
labelString = ",".join(labels)

## write to file
numpy.savetxt('data_processed/weather_raw.csv',weather,delimiter=",",fmt="%s",header=labelString)
