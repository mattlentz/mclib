#!/usr/bin/python

from agilent.dmm34411A.dmm34411A import dmm34411A
import time
import numpy

###########################################################################
# Configuration
collectionTime = 30*60 # Seconds
sampleFreq = 2000.0 # Hz
samplesPerTrigger = 1

currentSenseResistor = 0.173 # Ohms
###########################################################################

sampleAperture = 1.0 / (1.05 * sampleFreq)
totalSamples = collectionTime * sampleFreq

voltage = dmm34411A("192.168.1.203")
current = dmm34411A("192.168.1.204")
freq    = dmm34411A("192.168.1.205")

freq.setOutput(0)
freq.setSquare()
freq.setVoltage(0,3)
freq.setFrequency(sampleFreq/samplesPerTrigger)

voltage.setVoltageDC("10V", "MAX")
voltage.setVoltageDCAperture(str(sampleAperture))
voltage.setSamplesPerTrigger(str(samplesPerTrigger))
voltage.setTriggerSource("EXT")
voltage.setTriggerCount("INF")
voltage.setTriggerDelay("0")
voltage.setInitiate()

current.setVoltageDC("100mV", "MAX")
current.setVoltageDCAperture(str(sampleAperture))
current.setSamplesPerTrigger(str(samplesPerTrigger))
current.setTriggerSource("EXT")
current.setTriggerCount("INF")
current.setTriggerDelay("0")
current.setInitiate()

time.sleep(1)

freq.setOutput(1)

measuredI = []
measuredV = []
outputPos = 0

print "# Samples = %d"%(totalSamples)
print "# SampleRate = %f"%(sampleFreq)
print "# SampleAperture = %f"%(sampleAperture)

while (len(measuredI) < totalSamples) or (len(measuredV) < totalSamples):
    if len(measuredI) < totalSamples:
        measuredI += current.getMeasurements()
    if len(measuredV) < totalSamples:
        measuredV += voltage.getMeasurements()

    for i in range(outputPos,min(len(measuredI), len(measuredV))):
        print (measuredI[i] / currentSenseResistor), measuredV[i]

    outputPos = min(len(measuredI), len(measuredV))

    time.sleep(0.1)

freq.setOutput(0)

