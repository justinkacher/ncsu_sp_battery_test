import os
import pandas as pd
import numpy as np
import json
import statistics
import math


folder = '/Volumes/GoogleDrive-115458662593069358043/Shared drives/SolarPack/Teams/Electrical/Project Teams/Battery/Battery Test Plan/Partial Discharge/All Tested through April 23/partial_discharge'
#'/Volumes/GoogleDrive-115458662593069358043/Shared drives/SolarPack/Teams/Electrical/Project Teams/Battery/Battery Test Plan/Tested Batteries/partial_discharge'
masterFile = folder + '/Master_Data.json'

# folder = 'C:/Users/nwoodwa/Documents/SolarPack'
# masterFile = 'C:/Users/nwoodwa/Documents/SolarPack/Master_Data.json'


f = open(masterFile)
master = json.load(f)       # returns dictionary
# print(type(master))
# print(master)

# print(master.keys())		# returns a class of keys
master_keys = list(master.keys()) 	# list of keys
# print(master_keys)
# ['impedance', 'voc', 'resistance', 'cap_volt', 'cap_time']

## sorts list if needed
# for key in master_keys:
# 	master[key] = dict(sorted(master[key].items()))
#

cells_tested = list(master['voc'].keys())
print(cells_tested)
print(len(cells_tested)) # 1769

cells_tested = list(master['resistance'].keys())
print(cells_tested)
print(len(cells_tested)) # 1769


def save_dict(dict, name):
	df_dict = pd.DataFrame({key: pd.Series(value) for key, value in dict.items()})
	df_dict.to_excel(folder + '/' + name + '.xlsx')

## save as dict as excels
# save_dict(master['voc'],'Voc')
# save_dict(master['impedance'],'AC Impedance')
# save_dict(master['resistance'],'DC Resistance')
# save_dict(master['cap_volt'],'Partical Capacity Voltages')
# save_dict(master['cap_time'],'Partical Capacity Measurment Times')

## group cells into groups of 100 cells,
# assumes list is presorted

groupings = math.ceil(len(cells_tested)/100)		# math.ceil rounds up, math.floor rounds down #round rounds up or down at .5
print(groupings)
grouped = {}

skipped = []
for i in range(groupings):
	print(i)
	min = (100*i)
	max = (100*(i+1))

	# print(min)
	# print(max)
	cells = cells_tested[min:max]		# list of names of grouping
	# print(cells)
	g = []								# list of respective resistance

	for cell in cells:
		try:
			g.append(master['resistance'][cell])
		except:
			skipped.append(cell)
			print(cell)


	cells.append("Mean: ")
	cells.append("Stanard Dev: ")

	g_average = statistics.mean(g)
	g.append(g_average)
	g_std = statistics.stdev(g)
	g.append(g_std)


	grouped['Cells '+str(i+1)] = cells
	grouped['Resistance '+str(i+1)] = g

print(skipped)
print(len(skipped))

save_dict(grouped, "Resistance and mean")




