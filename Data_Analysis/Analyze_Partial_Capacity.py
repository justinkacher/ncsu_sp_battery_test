import os
import pandas as pd
import numpy as np
import json
import statistics
import math


folder = '/Volumes/GoogleDrive-115458662593069358043/Shared drives/SolarPack/Teams/Electrical/Project Teams/Battery/Battery Test Plan/Partial Discharge/All Tested through April 23/partial_discharge'
masterFile = folder + '/Master_Data.json'

# folder = 'C:/Users/nwoodwa/Documents/SolarPack'
# masterFile = 'C:/Users/nwoodwa/Documents/SolarPack/Master_Data.json'


f = open(masterFile)
master = json.load(f)       # returns dictionary
# print(type(master))
# print(master)


# master['cap_volt'],'Partical Capacity Voltages')
# master['cap_time'],'Partical Capacity Measurment Times')

cells_tested = list(master['cap_volt'].keys())

# Voltage vs Time
# it is assumed that a discharges

cap_slope = []
for cell in cells_tested:
	cap_volt = master['cap_volt'][cell]		# list of voltages
	cap_time = master['cap_time'][cell]		# list of times

	# slope =  dy / dx = ( volt[i+1] - volt[i] ) / ( cap_time[] )
	slope = []
	for i in range(len(cap_volt)):
		slope_i = ( cap_volt[i+1] - cap_volt[i] ) / ( cap_time[i+1] - cap_time[i] )
		slope.append(slope_i)

	print(statistics.mean(slope))
	print(cap_volt[-1] - cap_volt[0] ) / ( cap_time[-1] - cap_time[0])

	cap_slope.append(statistics.mean(slope))




