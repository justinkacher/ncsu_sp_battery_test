import os
import pandas as pd
import numpy as np
import json
import statistics
import math


folder = '/Volumes/GoogleDrive-115458662593069358043/Shared drives/SolarPack (1)/Teams/Electrical/Project Teams/Battery/Battery Test Plan/Tested Batteries/partial_discharge'
masterFile = folder + '/Master_Data.json'

def save_dict(dict, name):
	df_dict = pd.DataFrame({key: pd.Series(value) for key, value in dict.items()})
	df_dict.to_excel(folder + '/Excel/' + name + '.xlsx')

f = open(masterFile)
master = json.load(f)       # returns dictionary
# print(type(master))
# print(master)


# master['cap_volt'],'Partical Capacity Voltages')
# master['cap_time'],'Partical Capacity Measurment Times')

cells_tested = list(master['cap_volt'].keys())



# Voltage vs Time
# it is assumed that all discharged at 10amps
# capacityTest_dict = {}		# dictionary of each cell's capacity analysis; more dictionaries of voltage drop and slope calculation
# voltDrop_list = []
# capSlope_list = []
# for cell in cells_tested[:15]:
# 	cell_dict = {}
#
# 	cap_volt = master['cap_volt'][cell]		# list of voltages
# 	cap_time = master['cap_time'][cell]		# list of times
#
# 	# slope =  dy / dx = ( volt[i+1] - volt[i] ) / ( cap_time[] )
# 	slope = []
# 	for i in range(len(cap_volt)-1):
# 		slope_i = ( cap_volt[i+1] - cap_volt[i] ) / ( cap_time[i+1] - cap_time[i] )
# 		slope.append(slope_i)
#
# 	mean_slope = statistics.mean(slope)
# 	total_slope = (cap_volt[-1] - cap_volt[0]) / ( cap_time[-1] - cap_time[0])
# 	volt_drop = cap_volt[-1] - cap_volt[0]
#
# 	voltDrop_list.append(volt_drop)
# 	capSlope_list.append(mean_slope)
#
# 	cell_dict['mean slope'] = mean_slope
# 	cell_dict['total slope'] = total_slope
# 	cell_dict['volt drop'] = volt_drop
# 	cell_dict['Voc'] =  master['voc'][cell]
# 	cell_dict['DC Resistance'] = master['resistance'][cell]
# 	capacityTest_dict[cell] = cell_dict


# cap_json = json.dumps(capacityTest_dict, indent=4)
# print(cap_json)
#
# print(statistics.stdev(voltDrop_list))
# print(statistics.stdev(capSlope_list))

groupings = math.ceil(len(cells_tested)/100)		# math.ceil rounds up, math.floor rounds down #round rounds up or down at .5
print(groupings)
print(len(cells_tested))

grouped = {}
skipped = []

capacityTest_dict = {}		# dictionary of each cell's capacity analysis; more dictionaries of voltage drop and slope calculation
for g in range(groupings):
	min = (100*g)
	max = (100*(g+1))

	# print(min)
	# print(max)
	cells = cells_tested[min:max]		# list of names of grouping
	# print(cells)

	g_slope = []			# list of respective capacity slope
	g_voltDrop = []			# list of respecitive capacity drop
	g_slope = []
	g_voltDrop = []
	g_res = []
	g_voc = []
	g_imp = []

	for cell in cells:
		try:
			cell_dict = {}		# create a dict to hold each cells data; to be added to capacityTest_dict

			cap_volt = master['cap_volt'][cell]		# list of voltages
			cap_time = master['cap_time'][cell]		# list of times

			# slope =  dy / dx = ( volt[i+1] - volt[i] ) / ( cap_time[] )
			slope = []
			for i in range(len(cap_volt)-1):
				slope_i = ( cap_volt[i+1] - cap_volt[i] ) / ( cap_time[i+1] - cap_time[i] )
				slope.append(slope_i)

			# calculate the mean slope and general slope using first and last measurements
			mean_slope = statistics.mean(slope)
			total_slope = (cap_volt[-1] - cap_volt[0]) / (cap_time[-1] - cap_time[0])
			g_slope.append(mean_slope)

			# calculate the voltage drop from start to end of test
			volt_drop = cap_volt[-1] - cap_volt[0]
			g_voltDrop.append(volt_drop)

			g_res.append(master['resistance'][cell])

			g_voc.append(master['voc'][cell])

			g_imp.append(master['impedance'][cell])

			cell_dict['mean slope'] = mean_slope
			cell_dict['total slope'] = total_slope
			cell_dict['volt drop'] = volt_drop
			cell_dict['Voc'] = g_voc
			cell_dict['DC Resistance'] = g_res
			capacityTest_dict[cell] = cell_dict

		except:
			skipped.append(cell)
			print(cell + "Failed")

	# add mean and standard dev to bottom of columns, cell name list
	cells.append("Mean: ")
	cells.append("Standard Dev: ")

	# capacity slope average and std dev
	slope_average = statistics.mean(g_slope)
	slope_std = statistics.stdev(g_slope)
	g_slope.append(slope_average)
	g_slope.append(slope_std)

	# voltage drop average and std dev
	vdrop_average = statistics.mean(g_voltDrop)
	vdrop_std = statistics.stdev(g_voltDrop)
	g_voltDrop.append(vdrop_average)
	g_voltDrop.append(vdrop_std)

	# Resistance average and std dev
	res_average = statistics.mean(g_res)
	res_std = statistics.stdev(g_res)
	g_res.append(res_average)
	g_res.append(res_std)

	# Impedance average and std dev
	imp_aveage = statistics.mean(g_imp)
	imp_std = statistics.stdev(g_imp)
	g_imp.append(imp_aveage)
	g_imp.append(imp_std)

	# Voc average and std dev
	voc_average = statistics.mean(g_voc)
	voc_std = statistics.stdev(g_voc)
	g_voc.append(voc_average)
	g_voc.append(voc_std)

	grouped['Cells '+str(g+1)] = cells
	grouped['Voc'+str(g+1)] = g_voc
	grouped['DC Resistance'+str(g+1)] = g_res
	grouped['Voltage Drop'+str(g+1)] = g_voltDrop
	grouped['Capacity Slope '+str(g+1)] = g_slope
	grouped['AC Impedance'+str(g+1)] = g_imp

print(skipped)
print(len(skipped))

# save to excel
save_dict(grouped, 'Cell Comparision')


