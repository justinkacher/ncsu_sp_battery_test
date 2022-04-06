import os
import pandas as pd
import numpy as np
import json



### Test Files
# finds which test files are not currently in the



folder = 'C:/Users/nwoodwa/Documents/SolarPack'

# battery serial number is test
## tests are saved using: df_battery_dict.to_excel(fileFolder + '/Test cell ' + cell_Dict['Cell Number'] + '.xlsx') # line 113 Tkinter_master
folderContents = os.listdir(folder)    # returns list of folder and file name .Type for the specified folder
print(folderContents)

new_Files = []
for item in folderContents:
    if item[-4:] == "xlsx":
        new_Files.append(item)
    # cell_number = file[-16:-5]
    # update file with only new cells tested
    # get master file names
    # compare all fileNames to master file names
    # if not in master: add data

print(new_Files)

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

print(cell_number)

print(master['impedance'][cell_number])
print(master['voc'][cell_number])
print(master['resistance'][cell_number])
print(master['cap_volt'][cell_number])
print(master['cap_time'][cell_number])


print(master)



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
with open(folder +'/'+"Master_Data.json", "w") as outfile:
    json.dump(master, outfile)