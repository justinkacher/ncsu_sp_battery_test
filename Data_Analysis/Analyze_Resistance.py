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



cells_tested = list(master['resistance'].keys())

# total_res = []
# for cell in cells_tested:
# 	res = master['resistance'][cell]
# 	total_res.append(res)
#
# res_mean = 	statistics.mean(total_res)
# res_std = statistics.stdev(total_res)
#
#
# min = res_mean - res_std*3
# max = res_mean + res_std*3
#
# print(res_mean)
# print(res_std)
# print(min)
# print(max)
#
# out_of_range = {}
# for cell in cells_tested:
# 	res = master['resistance'][cell]
# 	if res < min or res > max:
# 		out_of_range[cell] = res
#
#
# print(out_of_range)
# print(len(out_of_range))
#
#
# Run 1
# 18.775770238345547
# 0.9782663915869813
# 16.819237455171585
# 20.73230302151951
# {'MP42A00151': 16.76631473855583, 'MP42A00160': 16.58839609445713, 'MP42A00165': 16.09857999196289, 'MP42A00214': 16.79968309287216, 'MP42A00242': 16.6040537209343, 'MP42A00253': 16.52636305589016, 'MP42A00262': 16.5707300961877, 'MP42A00327': 16.72286515385822, 'MP42A00412': 20.76707142893022, 'MP42A00413': 20.96045011141294, 'MP42A00415': 20.80586680487047, 'MP42A00428': 20.89128649772529, 'MP42A00810': 20.76585187795526, 'MP42A00820': 20.80147305144333, 'MP42A00830': 20.78242914921419, 'MP42A00839': 23.63523320086574, 'MP42A00840': 12.79554849075384, 'MP42A00870': 15.0509000926553, 'MP42A00937': 22.62005512184142, 'MP42A01001': 15.45423129406827, 'MP42A01034': 16.50395511673081, 'MP42A01123': 20.89906681805047, 'MP42A01135': 20.73809885652163, 'MP42A01144': 20.7915181568814, 'MP42A01145': 20.8347283346327, 'MP42A01174': 15.9608757636558, 'MP42A01201': 20.96703555136595, 'MP42A01202': 20.96019166300972, 'MP42A01214': 13.99095937108535, 'MP42A01295': 15.95304428841347, 'MP42A01408': 21.13813215806478, 'MP42A01413': 21.08256905213875, 'MP42A01428': 20.82035210896605, 'MP42A01488': 20.74051465009131, 'MP42A01515': 16.01735264708781, 'MP42A01535': 16.76066433205992, 'MP42A01558': 15.66296217355304, 'MP42A01562': 15.32522633347194, 'MP42A01563': 16.30627174015495, 'MP42A01566': 14.87419351340684, 'MP42A01596': 16.02738975635473, 'MP42A01602': 21.01478308934973, 'MP42A01603': 21.02353640249365, 'MP42A01606': 21.24356930501868, 'MP42A01608': 20.84813154112049, 'MP42A01613': 20.78479823494926, 'MP42A01614': 20.85584760229495, 'MP42A01615': 20.86159513969537, 'MP42A01617': 20.76705564118429, 'MP42A01618': 20.75153144720519, 'MP42A01624': 20.75466933858345, 'MP42A01626': 21.27687444216415, 'MP42A01629': 21.1202690267754, 'MP42A01638': 20.73928700455954, 'MP42A01648': 20.78589249764919, 'MP42A01756': 14.23761896742573}
# 56

# Run 2
# 18.788606871791586
# 0.9257370010037498
# 16.937132869784087
# 20.640080873799086
# {'MP42A00151': 16.76631473855583, 'MP42A00160': 16.58839609445713, 'MP42A00165': 16.09857999196289, 'MP42A00214': 16.79968309287216, 'MP42A00221': 16.82962954210054, 'MP42A00242': 16.6040537209343, 'MP42A00253': 16.52636305589016, 'MP42A00262': 16.5707300961877, 'MP42A00327': 16.72286515385822, 'MP42A00379': 16.92067981611475, 'MP42A00412': 20.76707142893022, 'MP42A00413': 20.96045011141294, 'MP42A00415': 20.80586680487047, 'MP42A00420': 20.68483442364445, 'MP42A00428': 20.89128649772529, 'MP42A00810': 20.76585187795526, 'MP42A00820': 20.80147305144333, 'MP42A00830': 20.78242914921419, 'MP42A00847': 20.68366699787388, 'MP42A00915': 16.84630475083893, 'MP42A00916': 16.89399209089728, 'MP42A01034': 16.50395511673081, 'MP42A01104': 20.645954797817, 'MP42A01118': 20.68276912781496, 'MP42A01123': 20.89906681805047, 'MP42A01133': 20.68377159429081, 'MP42A01135': 20.73809885652163, 'MP42A01136': 20.64584482976834, 'MP42A01138': 20.69257587745599, 'MP42A01144': 20.7915181568814, 'MP42A01145': 20.8347283346327, 'MP42A01147': 20.65490018661008, 'MP42A01174': 15.9608757636558, 'MP42A01201': 20.96703555136595, 'MP42A01202': 20.96019166300972, 'MP42A01295': 15.95304428841347, 'MP42A01408': 21.13813215806478, 'MP42A01413': 21.08256905213875, 'MP42A01428': 20.82035210896605, 'MP42A01488': 20.74051465009131, 'MP42A01515': 16.01735264708781, 'MP42A01535': 16.76066433205992, 'MP42A01563': 16.30627174015495, 'MP42A01584': 16.87602163816292, 'MP42A01596': 16.02738975635473, 'MP42A01602': 21.01478308934973, 'MP42A01603': 21.02353640249365, 'MP42A01606': 21.24356930501868, 'MP42A01608': 20.84813154112049, 'MP42A01610': 20.6525141915358, 'MP42A01613': 20.78479823494926, 'MP42A01614': 20.85584760229495, 'MP42A01615': 20.86159513969537, 'MP42A01617': 20.76705564118429, 'MP42A01618': 20.75153144720519, 'MP42A01624': 20.75466933858345, 'MP42A01625': 20.66028128652277, 'MP42A01628': 20.71807886561188, 'MP42A01629': 21.1202690267754, 'MP42A01636': 20.70250366472915, 'MP42A01638': 20.73928700455954, 'MP42A01647': 20.6748783585339, 'MP42A01648': 20.78589249764919}
# 63


# Pull out one cell that is close to mean for each 100
# group cells by number by 100

grouping = {}
for i in range(18):
	min_g = (100*i)
	max_g = (100*(i+1))

	g = {}
	for cell in cells_tested:
		cell_number = int(cell[-5:])

		if cell_number >= min_g and cell_number < max_g:
			g[cell] = master['resistance'][cell]

	grouping["Group: " +str(min_g) + " to " + str(max_g)] = g

group_Keys = list(grouping.keys())
# print(grouping)
# print(group_Keys)
# print(len(group_Keys))
# ['Group: 0 to 100', 'Group: 100 to 200', 'Group: 200 to 300', 'Group: 300 to 400', 'Group: 400 to 500', 'Group: 500 to 600', 'Group: 600 to 700', 'Group: 700 to 800', 'Group: 800 to 900', 'Group: 900 to 1000', 'Group: 1000 to 1100', 'Group: 1100 to 1200', 'Group: 1200 to 1300', 'Group: 1300 to 1400', 'Group: 1400 to 1500', 'Group: 1500 to 1600', 'Group: 1600 to 1700', 'Group: 1700 to 1800']
# 18 groups

mean_Res = 18.7886

for i in range(len(group_Keys)):
	group = grouping[group_Keys[i]]	# dict of values
	# print(group)
	# print(type(group))
	# print(group.items())

	cell_name, cell_res = min(group.items(), key=lambda kv: abs(kv[1] - mean_Res))

	print(cell_name + " " + str(cell_res))
	# print(cell_name)


