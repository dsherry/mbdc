#!/usr/bin/python
import numpy
import csv
import datetime
import matplotlib
import matplotlib.pyplot as plt

## read in training points
zones = numpy.array([[-71.057114,42.343365],
[-71.02861,42.344254],
[-71.064461,42.350315],
[-71.114105,42.300732],
[-71.062103,42.366261],
[-71.016518,42.366631],
[-71.055138,42.351818],
[-71.056213,42.360039],
[-71.127762,42.358086],
[-71.06559,42.350483],
[-71.040916,42.346043],
[-71.040306,42.351776],
[-71.04924,42.359219],
[-71.060493,42.355457],
[-71.073502,42.347263],
[-71.056396,42.357574],
[-71.051659,42.345394],
[-71.083717,42.329704],
[-71.075111,42.347534],
[-71.065109,42.35154],
[-71.059608,42.3592],
[-71.062569,42.354008],
[-71.036064,42.348522],
[-71.064713,42.350712],
[-71.049767,42.351658],
[-71.066193,42.349987],
[-71.053635,42.359726],
[-71.097244,42.346439],
[-71.04493,42.346577],
[-71.065567,42.315872],
[-71.084206,42.347626],
[-71.055511,42.365353],
[-71.08567,42.342808],
[-71.04525,42.353764],
[-71.042946,42.352856]])

## read in raw training data
print "loading training data"
train = numpy.loadtxt('data_original/pickups_train.csv',delimiter=',',dtype=object)
## timestamp, long, lat
train_trimmed = numpy.vstack([train[:,1], numpy.array(train[:,3],dtype=float),numpy.array(train[:,4],dtype=float)]).transpose()
print "loaded training data"


## check each row against the 36 reference points
# for row in xrange(len(train_trimmed)):
#     row_zones = numpy.apply_along_axis(lambda r: (r[0]-row[1])**2 + ()

# matrix ops:
# for each zone, calculate the indices for which pickups are in the correct region
# then add duplicate rows to some other variable
master_list=numpy.array([]).reshape((0,4))
for i,zone in enumerate(zones):
    print "Working on zone " + str(i) + " with coords " + str(zone)
    zone_list = numpy.array([]).reshape((0,3))
    lon = numpy.array(train_trimmed[:,1],dtype=float)
    lat = numpy.array(train_trimmed[:,2],dtype=float)
    zone_threshold_indices = (0.00224946357 > numpy.sqrt(numpy.power(lon - zone[0],2) + numpy.power(lat - zone[1],2)))
    print "Obtained %s rows which match the threshold" %(numpy.sum(zone_threshold_indices))

    # grab the rows we care about
    zone_cols = train_trimmed[zone_threshold_indices,:]
    # add an extra column which is "zone id"
    zone_cols = numpy.hstack([zone_cols,numpy.ones((zone_cols.shape[0],1),dtype=int)*i])

    # add these rows to the master_list
    master_list = numpy.vstack([master_list,zone_cols])

## group by date


# morning of may 1st 2012
initial_date = datetime.datetime(2012,5,1)

# hours range from 0 to 5136, cols are zones
aggregates = numpy.zeros((5137,35))
for i,row in enumerate(master_list):
    ## translate the date
    timestamp = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
    elapsed_hours = int(numpy.round((timestamp - initial_date).total_seconds() / 3600.0))

    zone = row[3]

    ## use the elapsed_hours to index into the aggregation array
    ## first do the current hour
    aggregates[elapsed_hours,zone] += 1
    if elapsed_hours > 1: aggregates[elapsed_hours] += 1

holidays=['2012-05-28','2012-07-04','2012-09-03','2012-10-08','2012-11-12','2012-11-22']

# write out the output
final_output = numpy.zeros((aggregates.shape[0] * aggregates.shape[1],6),dtype=object)
for hours,row in enumerate(aggregates):
    timestamp = initial_date + datetime.timedelta(0, hours*3600)
    date_str = str(timestamp.date())
    hour = timestamp.hour
    minutes_since_may1 = (timestamp - initial_date).total_seconds() / 60.0
    is_holiday = int(date_str in holidays)
    for zone,count in enumerate(row):
        final_output[(aggregates.shape[1]*hours)+zone,:] = numpy.array([[date_str, hour, int(minutes_since_may1), is_holiday, zone, int(count)]],dtype=object)

## write to file
numpy.savetxt('train_dylan.csv',final_output,delimiter=',',fmt='%s')
