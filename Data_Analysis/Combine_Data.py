import os
import pandas as pd
import numpy as np



### Test Files
# finds which test files are not currently in the



folder = ' '

# battery serial number is test
## tests are saved using: df_battery_dict.to_excel(fileFolder + '/Test cell ' + cell_Dict['Cell Number'] + '.xlsx') # line 113 Tkinter_master
fileNames = os.listdir(folder)    # returns list of file name and .Type for specified folder


# update file with only new cells tested
# get master file names
# compare all fileNames to master file names
# if not in master: add data
new_Files = fileNames




# open master files
# xls = pd.ExcelFile('{}/{}.xlsx'.format(folder, file))
# df_measurements = pd.read_excel(xls, 'Voc')


df_measurements = {}
resitance_dict = {}



##df4 = df4.reindex(range( max(len(df4), len(c)) ))
##df4['three'] = pd.Series(c)




# open test file and save data to master
# file name: '/Test cell ' + cell_Dict['Cell Number'] + '.xlsx'
# Data:
# cell_Dict['Analog Impedence'] is a float
# cell_Dict['Voc (V)'] is a float
# cell_Dict['DC Resistance (Ohms)'] is a float
# cell_Dict.update({'Capacity Time': time_list, 'Capacity Voltage': voltage_list})

impedance = {}
voc = {}
resistance = {}
cap_volt_list = {}
cap_time_list = {}

for file in new_Files:
    cell_number = file[-16:-5]  # Test cell [cell number]

    xls = pd.ExcelFile('{}/{}.xlsx'.format(folder, file))
    df_measurements = pd.read_excel(xls)

    impedance[cell_number] = df_measurements['Analog Impedence']
    voc[cell_number] = df_measurements['Voc (V)']
    resistance[cell_number] = df_measurements['DC Resistance (Ohms)']
    cap_volt_list[cell_number] = df_measurements['Capacity Voltage']
    cap_time_list[cell_number] = df_measurements['Capacity Time']








skipped = []        # list of files skipped due to error

# run Dual analysis for each file
for file in fileNames:
    print(file)
    filePath = folder + "/" + file
    savePath = folder + '/Corrected V0.2/' + file[:-5]         # [:-5] removes the .xlsx from the name

    try:
        dam.daul_analysis(filePath, savePath)
    except:
        print("Skipped")
        skipped.append(file)

print(skipped)


## Saving

# Serializing json
# json_object = json.dumps(dictionary, indent = 4)
# print(json_object)