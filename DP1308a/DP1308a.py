import time
import requests
import xml.etree.ElementTree as ET

class DP1308a:
	url = 'http://{0}.eecs.umich.edu/lxi/infomation.xml?{1}&timeStamp={2}'
	hostname = ''
	
	def __init__ (self, hostname):
		self.hostname = hostname

	def send_function (self, function_id):
		timestamp = long(time.time()*1000)
		url = self.url.format(self.hostname, function_id, timestamp)
		req = requests.get(url)
		return req

	def sf (self, function_id):
		self.send_function(function_id)

	def check_field (self, field):
		req = self.send_function(0)
		return ET.XML(req.content).find(field).text

	def check_rail_power (self, rail, value):
		names = ['P6STAT', 'P25STAT', 'N25STAT']
		rail = int(rail)
		if rail >= 0 and rail <= 2:
			return self.check_field(names[rail]) == value

	def check_rail_on (self, rail):
		return self.check_rail_power(rail, 'ON')

	def check_rail_off (self, rail):
		return self.check_rail_power(rail, 'OFF')

	def set_rail_power (self, rail, turn_on=True):
		power_buttons = [8273, 8241, 8257]
		rail = int(rail)
		if rail >= 0 and rail <= 2:
			if not self.check_rail_power(rail, ('OFF', 'ON')[turn_on]):
				self.sf(power_buttons[rail])

	def set_rail_on (self, rail):
		self.set_rail_power(rail, True)

	def set_rail_off (self, rail):
		self.set_rail_power(rail, False)

	def set_all_off (self):
		self.sf(8225)
		self.enter_ok()

	def set_voltage (self, rail, voltage):
		if rail == 0 and voltage >= 0.0 and voltage <= 6.0:
			self.sf(4129)	# switch to the 6V rail
		elif rail == 1 and voltage >= 0.0 and voltage <= 25.0:
			self.sf(4097)	# switch to the 25V rail
		elif rail == 2 and voltage <= 0.0 and voltage >= -25.0:
			self.sf(4113)	# switch to the -25V rail
		else:
			return

		self.set_rail_on(rail)
		self.sf(12289)		# switch to voltage
		self.enter_number(voltage)
		self.enter_ok()

	def set_current (self, rail, current):
		if rail == 0 and current >= 0.0 and current <= 5.0:
			self.sf(4129)	# switch to the 6V rail
		elif rail == 1 and current >= 0.0 and current <= 1.0:
			self.sf(4097)	# switch to the 25V rail
		elif rail == 2 and current >= 0.0 and current <= 1.0:
			self.sf(4113)	# switch to the -25V rail
		else:
			return

		self.set_rail_on(rail)
		self.sf(12305)		# switch to current
		self.enter_number(current)
		self.enter_ok()

	def enter_number (self, num):
		val = str(num)
		for c in val:
			if c == '.':
				self.enter_decimal()
			else:
				self.enter_digit(int(c))

	def enter_digit (self, num):
		val = int(num)
		num_ids = [16385, 16401, 16417, 16433, 16449, 16465, 16481, 16497, 16513, 16529]
		if (num >= 0 and num <= 9):
			self.sf(num_ids[val])

	def enter_decimal (self):
		self.sf(16545)

	def enter_ok (self):
		self.sf(8305)



ps = DP1308a('lab4908ps01')
ps.set_voltage(1, 1.0)
#ps.set_all_off()
