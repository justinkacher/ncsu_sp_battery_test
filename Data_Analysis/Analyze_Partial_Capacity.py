import os
import pandas as pd
import numpy as np
import json
import statistics
import math


folder = '/Volumes/GoogleDrive-115458662593069358043/Shared drives/SolarPack (1)/Teams/Electrical/Project Teams/Battery/Battery Test Plan/Tested Batteries/partial_discharge'
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

capacityTest_dict = {}		# dictionary of each cell's capacity analysis; more dictionaries of voltage drop and slope calculation
for cell in cells_tested[:15]:
	cell_dict = {}

	cap_volt = master['cap_volt'][cell]		# list of voltages
	cap_time = master['cap_time'][cell]		# list of times

	# slope =  dy / dx = ( volt[i+1] - volt[i] ) / ( cap_time[] )
	slope = []
	for i in range(len(cap_volt)-1):
		slope_i = ( cap_volt[i+1] - cap_volt[i] ) / ( cap_time[i+1] - cap_time[i] )
		slope.append(slope_i)

	mean_slope = statistics.mean(slope)
	total_slope = (cap_volt[-1] - cap_volt[0]) / ( cap_time[-1] - cap_time[0])
	volt_drop = cap_volt[-1] - cap_volt[0]


	cell_dict['mean slope'] = mean_slope
	cell_dict['total slope'] = total_slope
	cell_dict['volt drop'] = volt_drop
	cell_dict['Voc'] =  master['voc'][cell]
	cell_dict['DC Resistance'] = master['resistance'][cell]

	capacityTest_dict[cell] = cell_dict

# print(capacityTest_dict)

cap_json = json.dumps(capacityTest_dict, indent=4)
print(cap_json)



