import csv
import sys


def max_value(inputlist, i):
	return max([sublist[i] for sublist in inputlist])

START_DATE = 0
END_DATE = 1
CATEGORY = 2
START = 3
STOP = 4
MILES = 5
PURPOSE = 6
DURATION = 7

with open('MyUberDrives-2016.csv', 'rb') as csvfile:
	rawInput = csv.reader(csvfile, delimiter=',')
	headers = rawInput.next()
	print headers

	i = 0
	rides = []
	trainData = []
	testData = []
	trainLabel = []
	testLabel = []
	for row in rawInput:
		rides.append(row)
		i = i+1

	totalRides = len(rides)
	data = list(rides)
	data.pop()

	from random import shuffle
	shuffle(data)

# Create train/test dataset 80/20
	trainSize = int(totalRides*0.8)
	testSize = totalRides - trainSize - 1

	for eachRide in range(0, totalRides-1):
		x = data[eachRide][PURPOSE]
# Label purpose as follows
# 0 Meal/Entertain
# 1 Errand/Supplies
# 2 Meeting
# 3 Customer Visit
# 4 Temporary Site
# 5 Between Offices
# 6 Charity ($)
# 7 MOving
# 8 Commute
		data[eachRide][PURPOSE] = \
			0 if x=='Meal/Entertain' else  \
			 1 if x=='Errand/Supplies' else\
		 	2 if x=='Meeting' else\
			 3 if x=='Customer Visit' else\
			 4 if x=='Temporary Site' else\
		 	5 if x=='Between Offices' else\
			6 if x=='Charity ($)' else\
			7 if x=='Moving' else\
			8 if x=='Airport/Travel' else -1

		y = data[eachRide][CATEGORY]
		data[eachRide][CATEGORY] = 0 if y=='Business' else\
			1 if y=='Personal' else x
		z = data[eachRide][MILES]
		data[eachRide][MILES] = float(z)
		
		data[eachRide].pop(START)
		data[eachRide].pop(START)


 	
# Calculate duration using start and end time
		from datetime import datetime

		s = datetime.strptime(data[eachRide][START_DATE], '%m/%d/%Y %H:%M')
		e = datetime.strptime(data[eachRide][END_DATE], '%m/%d/%Y %H:%M')
		d = (e-s).seconds
		t=s.hour
		data[eachRide].append(d)
		data[eachRide].append(0 if (t>9 and t<17) else 1)
#remove start and end time and add duration in seconds
#and add time of day: morning, afteroon, 12:01am to 11:59am is morning
		data[eachRide].pop(0)
		data[eachRide].pop(0)

# Category, Miles, Purpose, Duration
# Add the first 80% rows in train, the rest goes into test

		if (eachRide<trainSize):
			trainData.append(data[eachRide])
			trainLabel.append(data[eachRide][4])
		else:
			testData.append(data[eachRide])
			testLabel.append(data[eachRide][4])
		
# removey daytime from features, this needs to be predicted based on other four features
	for i in range(0, trainSize):
		trainData[i].pop()
	for i in range(0, testSize):
		testData[i].pop()
	
#normalize distance and duration 0-1
maxDist=max_value(trainData, -3)
maxTime=float(max_value(trainData, -1))

for i in range(0, trainSize):
	trainData[i][1]=trainData[i][1]/maxDist
	trainData[i][3]=float(trainData[i][3])/maxTime

maxDist=max_value(testData, -3)
maxTime=float(max_value(testData, -1))

for i in range(0, testSize):
	testData[i][1]=testData[i][1]/maxDist
	testData[i][3]=float(testData[i][3])/maxTime

print len(trainData)
print len(testData)
print len(data)

# category, miles, purpose, duration, day time
# Classify the rides as Business 0 or Personal 1 based on three features: miles, duration and purpose
# Use support vector machine
from sklearn import svm
clf = svm.SVC(kernel='linear', C=0.1)
result = clf.fit(trainData, trainLabel).predict(testData)

print(testLabel)
print(result)
print(trainLabel)
#compute accuracy
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
print accuracy_score(testLabel, result)
print confusion_matrix(testLabel, result)
