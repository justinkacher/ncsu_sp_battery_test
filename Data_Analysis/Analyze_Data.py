import os
import pandas as pd
import numpy as np
import json


folder = 'Q:\Shared drives\SolarPack\Teams\Electrical\Project Teams\Battery\Battery Test Plan\Tested Batteries\partial_discharge'
masterFile = folder + '/Master_Data.json'

# folder = 'C:/Users/nwoodwa/Documents/SolarPack'
# masterFile = 'C:/Users/nwoodwa/Documents/SolarPack/Master_Data.json'


f = open(masterFile)
master = json.load(f)       # returns dictionary

# print(type(master))
# print(master)
# print(len(master['impedance'])) # 1494



