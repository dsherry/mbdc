#!/usr/bin/python
import numpy
import csv
import datetime
import matplotlib
import matplotlib.pyplot as plt

# read josep's training data into numpy

## days since jesus
#datetime.datetime.strptime('2012-05-02','%Y-%m-%d').date().toordinal()

train_josep_file = open('data_processed/train_josep.csv','r')
n_lines = len(train_josep_file.readlines()) - 1 ## ignore first line
train_josep = numpy.zeros((n_lines,4))
train_josep_reader = csv.reader(open('data_processed/train_josep.csv','r'))
## skip first line with labels
train_josep_reader.next()

n = 0
## read in data
for line in train_josep_reader:
    segs = line[0].split(" ")
    train_josep[n,0] = datetime.datetime.strptime(segs[0],'%Y-%m-%d').date().toordinal()
    for i in range(1,len(segs)):
        train_josep[n,i] = int(segs[i])
    n += 1


## calculate histograms for each variable
hour_counts,hour_bins=numpy.histogram(numpy.array(train_josep[:,1],dtype=int), bins=24)
zone_counts,zone_bins=numpy.histogram(numpy.array(train_josep[:,2],dtype=int), bins=34)
count_counts,count_bins=numpy.histogram(numpy.array(train_josep[:,3],dtype=int), bins=70)

plt.hist(count_counts,count_bins)
