#!/usr/bin/python

# Simple python data grabber.
import json
import os
import sys
from tektronix.miso2024.miso2024 import Miso2024

def rangeFromString(cmdVar):
	ret = set()
	for s in cmdVar.split(','):
		ss = s.split('-')
		ret.update(range(int(ss[0]), int(ss[-1])+1))
	return sorted(ret)

def doReceiveRangeFromUser(valid):
	while True:
		inputString = sys.stdin.readline().strip()
		inputRange = []
		try:
			inputRange = rangeFromString(inputString)
		except:
			print 'Invalid input, please try again'
			continue
		if not (False in map(lambda x: x in valid, inputRange)):
			return inputRange
		print 'Invalid input, please try again'

# Check for file name argument
if len(sys.argv) < 3:
	print 'Usage: {0} <scope host name> <output file name>'.format(sys.argv[0])
	quit()

scope = sys.argv[1].strip()
output_name = sys.argv[2].strip()

# Collect some data from the user.
print 'What is a short description of this data?'
dataDesc = sys.stdin.readline().strip()

#print 'Which scopes would you like to collect data from?'
#for i in range(len(hostList)):
#	print 'Scope %d: %s' % (i, hostList[i])
#print 'You can specify any sort of range, i.e. 1-2 or 2,3'

print 'Which channels would you like to collect from?'
print 'You can enter a range. i.e. 1-4'
print 'This list of channels will be collected from each scope.'

channels = doReceiveRangeFromUser(range(1,5))

# Begin the actual collection of the data
print 'Collecting data from scope... this will take a moment'
print 'Data collection typically takes a long time per channel.'

outputData = []
for i in channels:
	miso = Miso2024(scope)
	dataSet = miso.doDownloadData(i)
	print 'Recieved data set for channel {0} (sample row): {1}' \
	      .format(i, json.dumps(dataSet[0]))
	outputData.append(dataSet)

finalOutput = []

offset = 2e-3

for l in range(len(outputData[0])):
	listOfData = []
	listOfData.append(str(float(str(outputData[0][l][0]))))
	for c in range(len(outputData)):
		listOfData.append(str(float(str(outputData[c][l][1]))))
	finalOutput.append(listOfData)

out = open(output_name + ".dat", 'w')
descOut = open(output_name + ".desc", 'w')
descOut.write('Scope: {0}\n'.format(scope))
descOut.write('Channels: {0}\n'.format(json.dumps(channels)))
descOut.write('Description: {0}\n'.format(dataDesc))

for l in finalOutput:
	out.write(' '.join(l) + '\n')

descOut.close()
out.close()
