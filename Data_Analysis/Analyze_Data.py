import os
import pandas as pd
import numpy as np
import json


folder = '/Volumes/GoogleDrive-115458662593069358043/Shared drives/SolarPack/Teams/Electrical/Project Teams/Battery/Battery Test Plan/Tested Batteries/partial_discharge'
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

# for key in master_keys:
# 	master[key] = dict(sorted(master[key].items()))
#

cells_tested = list(master['voc'].keys())
# print(cells_tested)
# print(len(cells_tested)) # 1493


# def save_dict(dict, name):
# 	df_dict = pd.DataFrame({key: pd.Series(value) for key, value in dict.items()})
# 	df_dict.to_excel(folder + '/' + name + '.xlsx')
#
#
# save_dict(master['voc'],'Voc')
# save_dict(master['impedance'],'AC Impedance')
# save_dict(master['resistance'],'DC Resistance')
# save_dict(master['cap_volt'],'Partical Capacity Voltages')
# save_dict(master['cap_time'],'Partical Capacity Measurment Times')





