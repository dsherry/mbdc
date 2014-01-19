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
cols = len(non_numerical_keys + numerical_keys + ignored_keys)

## preallocate the python array
weather = numpy.zeros((n,cols), dtype=object)

## iterate over day
n = 0
for day in weather_raw:
    ## iterate over observation
    for obs in day['history']['observations']:
        utcdate = obs['date']
        date = datetime.datetime(int(utcdate['year']), int(utcdate['mon']), int(utcdate['mday']), int(utcdate['hour']), int(utcdate['min']))
        tdiff_since_0AD = (date - zeroAD)
        hours_since_0AD = tdiff_since_0AD.total_seconds() / 3600.0
        weather[n,0] = hours_since_0AD
        ## handle all non-numerical fields
        i = 1
        for key in non_numerical_keys:
            weather[n,i] = obs[key].lower()
            i += 1
        for key in numerical_keys:
            weather[n,i] = float(obs[key])
            i += 1
        n += 1

## get labels
labelString = ",".join([u'hours_since_0AD_est'] + non_numerical_keys + numerical_keys)

## write to file
numpy.savetxt('data_processed/weather_raw.csv',weather,delimiter=",",fmt="%s",header=labelString)
