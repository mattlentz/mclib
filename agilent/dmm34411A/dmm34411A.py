import socket
import time
import struct

class dmm34411A:
	PORT = 5025
	
	def __init__(self, host, port=PORT):
		self.host = host
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host, port))
	
		self.f = self.s.makefile("rb")
	
		#RESET
		self.s.send("*RST\n")
		self.s.send("*CLS\n")
	
		#set output load
		self.s.send("OUTPut:LOAD INF\n")
	
	def setSquare(self):
		#square function
		self.s.send("FUNCtion SQUare\n")
		
	def setSin(self):
		#sine function
		self.s.send("FUNCtion SIN\n")
	
	def setVoltage(self, low, high):
		#set initial voltage
		self.s.send("VOLTage:HIGH %.2f\n"%(high,))
		self.s.send("VOLTage:LOW %.2f\n"%(low,))

	def setVoltagePP(self, PP):
		self.s.send("VOLT %.2f VPP\n" % (PP))
	
	def setFrequency(self, freq):
		#set initial frequency
		self.s.send("FREQuency %.2f\n"%(freq,))
	
	def setLinSweep(self, start, stop, time):
		#set linear sweep with the specified start/stop freqs
		self.s.send("FREQ:STAR %.2f\n"%(start,))
		self.s.send("FREQ:STOP %.2f\n"%(stop,))
		self.s.send("SWE:SPAC LIN\n")
		self.s.send("SWE:TIME %.3f\n"%(time,))
		self.s.send("SWE:STAT ON\n")

	def setLoad(self, ohms):
		MIN = 1
		MAX = 10000
		if ohms is None:
			ohms = "INF"
		elif (ohms < MIN):
			print "Warning: Minimum load is 1ohm. Set to 1."
			ohms = "1"
		elif (ohms > MAX):
			print "Warning: Maximum load is 10kohm. Set to 10K."
			print "         To set to HighZ mode, set ohms=None"
			ohms = "10000"
		else:
			ohms = str(ohms)

		self.s.send("OUTPut:LOAD %s\n" % (ohms))

	def setOutput(self, status):
		if status:
			#enable the output
			self.s.send("OUTPut ON\n")
		else:
			self.s.send("OUTPut OFF\n")

# following are for the agilent multimeters A34410a
	def setCurrentDC(self, limit="AUTO", precision=""):
		if precision == "":
			self.s.send("CONF:CURR:DC AUTO\n")
		else:
			self.s.send("CONF:CURR:DC %s,%s\n"%(limit, precision))
			self.s.send("FORMAT REAL, 64\n")
	
	def setVoltageDC(self, limit="AUTO", precision=""):
		if precision == "":
			self.s.send("CONF:VOLT:DC AUTO\n")
		else:
			self.s.send("CONF:VOLT:DC %s,%s\n"%(limit, precision))
		self.s.send("FORMAT REAL, 64\n")
	
	def setVoltageAC(self, limit="AUTO", precision=""):
		if precision == "":
			self.s.send("CONF:VOLT:AC AUTO\n")
		else:
			self.s.send("CONF:VOLT:AC %s,%s\n"%(limit, precision))
		self.s.send("FORMAT REAL, 64\n")
	
	def setTriggerSource(self, source="EXT"):
		self.s.send("TRIGGER:SOURCE %s\n"%(source,))
	
	def setTriggerCount(self, count="INF"):
		self.s.send("TRIGGER:COUNT %s\n"%(count,))
	
	def setInitiate(self):
		self.s.send("INIT\n")

	def getSingleMeasurement(self):
		self.s.send("FETC?\n")
		r = ""
		while '\n' not in r:
			r += self.s.recv(1)

		return r

	def getMeasurements(self):
		self.s.send("R?\n")
		c = self.s.recv(1)
		if c != "#":
			print "*%s*"%(c,)
			return ""
		# read the number of digits that follow
		l = int(self.s.recv(1))
		length = int(self.s.recv(l))
	
		l = 0
		r = ""
		while l < int(length):
			c = self.s.recv(int(length)-l)
			l += len(c)
			r += c
	
		# read the newline character
		self.s.recv(1)

		print "l",l
		print "r",r
	
		m = struct.unpack(">%dd"%(int(length)/8,), r)
	
		return m

