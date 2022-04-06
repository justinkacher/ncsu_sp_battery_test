import os
import pandas as pd
import numpy as np
import json



### Test Files
# finds which test files are not currently in the

folder = 'Q:\Shared drives\SolarPack\Teams\Electrical\Project Teams\Battery\Battery Test Plan\Tested Batteries\partial_discharge'
masterFile = folder + '/Master_Data.json'

# folder = 'C:/Users/nwoodwa/Documents/SolarPack'
# masterFile = 'C:/Users/nwoodwa/Documents/SolarPack/Master_Data.json'


# battery serial number is test
## tests are saved using: df_battery_dict.to_excel(fileFolder + '/Test cell ' + cell_Dict['Cell Number'] + '.xlsx') # line 113 Tkinter_master
folderContents = os.listdir(folder)    # returns list of folder and file name .Type for the specified folder
# print(folderContents)

new_Files = []
for item in folderContents:
    if item[-4:] == "xlsx":
        new_Files.append(item)
    # cell_number = file[-16:-5]
    # update file with only new cells tested
    # get master file names
    # compare all fileNames to master file names
    # if not in master: add data

# print(new_Files)

# open master files
# xls = pd.ExcelFile('{}/{}.xlsx'.format(folder, file))
# df_measurements = pd.read_excel(xls, 'Voc')


##df4 = df4.reindex(range( max(len(df4), len(c)) ))
##df4['three'] = pd.Series(c)


# open test file and save data to master
# file name: '/Test cell ' + cell_Dict['Cell Number'] + '.xlsx'
# Data:
# cell number
# cell_Dict['Analog Impedence'] is a float
# cell_Dict['Voc (V)'] is a float
# cell_Dict['DC Resistance (Ohms)'] is a float
# cell_Dict.update({'Capacity Time': time_list, 'Capacity Voltage': voltage_list})

master = {'impedance': {}, 'voc': {}, 'resistance': {}, 'cap_volt': {}, 'cap_time':{}}
skipped = []

for file in new_Files:
    try:
        xls = pd.ExcelFile('{}/{}'.format(folder, file))
        df_measurements = pd.read_excel(xls)

        cell_number = df_measurements['Cell Number'].iloc[0]
        # cell_number = file[-16:-5]  # Test cell [cell number]

        master['impedance'][cell_number] = df_measurements['Analog Impedence'].iloc[0]
        master['voc'][cell_number] = df_measurements['Voc (V)'].iloc[0]
        master['resistance'][cell_number] = df_measurements['DC Resistance (Ohms)'].iloc[0]
        master['cap_volt'][cell_number] = df_measurements['Capacity Voltage'].to_list()
        master['cap_time'][cell_number] = df_measurements['Capacity Time'].to_list()
    except:
        skipped.append(file)

print(skipped)
# 51
#['Test cell MP42A01558.xlsx', 'Test cell MP42A01523.xlsx', 'Test cell MP42A01550.xlsx', 'Test cell MP42A01546.xlsx', 'Test cell MP42A01559.xlsx', 'Test cell MP42A01543.xlsx', 'Test cell MP42A01521.xlsx', 'Test cell MP42A01552.xlsx', 'Test cell MP42A01555.xlsx', 'Test cell MP42A01565.xlsx', 'Test cell MP42A01556.xlsx', 'Test cell MP42A01522.xlsx', 'Test cell MP42A01529.xlsx', 'Test cell MP42A01562.xlsx', 'Test cell MP42A01531.xlsx', 'Test cell MP42A01551.xlsx', 'Test cell MP42A01544.xlsx', 'Test cell MP42A01554.xlsx', 'Test cell MP42A01539.xlsx', 'Test cell MP42A01563.xlsx', 'Test cell MP42A01549.xlsx', 'Test cell MP42A01564.xlsx', 'Test cell MP42A01530.xlsx', 'Test cell MP42A01542.xlsx', 'Test cell MP42A01548.xlsx', 'Test cell MP42A01533.xlsx', 'Test cell MP42A01515.xlsx', 'Test cell MP42A01545.xlsx', 'Test cell MP42A01528.xlsx', 'Test cell MP42A01535.xlsx', 'Test cell MP42A01537.xlsx', 'Test cell MP42A01527.xlsx', 'Test cell MP42A01524.xlsx', 'Test cell MP42A01525.xlsx', 'Test cell MP42A01561.xlsx', 'Test cell MP42A01517.xlsx', 'Test cell MP42A01518.xlsx', 'Test cell test MP42A01553.xlsx', 'Test cell MP42A01547.xlsx', 'Test cell MP42A01536.xlsx', 'Test cell MP42A01557.xlsx', 'Test cell MP42A01516.xlsx', 'Test cell MP42A01532.xlsx', 'Test cell MP42A01540.xlsx', 'Test cell MP42A01519.xlsx', 'Test cell MP42A01526.xlsx', 'Test cell MP42A01541.xlsx', 'Test cell MP42A01560.xlsx', 'Test cell MP42A01534.xlsx', 'Test cell MP42A01538.xlsx', 'Test cell MP42A01520.xlsx']

# print(cell_number)
#
# print(master['impedance'][cell_number])
# print(master['voc'][cell_number])
# print(master['resistance'][cell_number])
# print(master['cap_volt'][cell_number])
# print(master['cap_time'][cell_number])
#
#
# print(master)



#
#
# # run Dual analysis for each file
# for file in fileNames:
#     print(file)
#     filePath = folder + "/" + file
#     savePath = folder + '/Corrected V0.2/' + file[:-5]         # [:-5] removes the .xlsx from the name
#
#     try:
#         dam.daul_analysis(filePath, savePath)
#     except:
#         print("Skipped")
#         skipped.append(file)
#
# print(skipped)
#
#
# ## Saving
#
# create json
# json_object = json.dumps(master, indent=4)
# print(json_object)

# save .json
with open(masterFile, "w") as outfile:
    json.dump(master, outfile)