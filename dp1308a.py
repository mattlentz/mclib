from rigol.DP1308a.DP1308a import DP1308a

ps = DP1308a('lab4908ps01.eecs.umich.edu')

# set the red supply to 5 volts
ps.set_voltage(0, 5.0)
