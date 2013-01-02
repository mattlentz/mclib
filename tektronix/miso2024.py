
import urllib2

# Class for tek scopes
class Miso2024 ():
	def __init__ (self, scope_host_name):
		self.ip = scope_host_name
		try:
			req = urllib2.Request('http://' + self.ip)
			urllib2.urlopen(req)
		except:
			raise Exception('Error: Could not connect to {0}'.format(self.ip))

	def doDownloadData(self, channel):
		url = 'http://' + self.ip + '/data/Tek_CH' + str(channel) + '_Wfm.csv'

		# The format of this payload comes from a Wireshark capture from the scope.
		# It's not a standard POST request.
		data = """WFMFILENAME=CH""" + str(channel) + """\r
WFMFILEEXT=csv\r
command=select:control ch""" + str(channel) + """\r
command1=save:waveform:fileformat spreadsheet\r
command2=:data:resolution full;:save:waveform:spreadsheet:resolution full\r
wfmsend=Get\r\n"""

		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		rawData = response.read()

		lines = rawData.split('\n')
		lines = map(lambda x: x.strip().split(','), lines)

		return lines[16:-3]
