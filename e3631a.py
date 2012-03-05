import sys
from agilent.E3631A.E3631A import E3631a

if len(sys.argv) < 2:
	print "Usage: python " + sys.argv[0] + " <device serial port>"
	sys.exit(1)

ea = E3631A(sys.argv[1])
ea.setVoltageCurrentP6(5, 1)

