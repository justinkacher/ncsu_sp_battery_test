from collections import namedtuple
#from distutils.log import error
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import simpledialog
from tkinter.constants import *
from tkinter.ttk import Labelframe
import os

import time

from matplotlib.pyplot import title
#from matplotlib import scale
#import tkcommands
# import config
# import scaletest
#from PIL import *
import Battery_Test_Methods_Ether as BTM
import pandas as pd
from statistics import mean
import scaletest
i

fileFolder = "/home/pi/Documents/solarpack/partial_discharge"

cell_Name = ""
mass = 0 


def scan_cell():
    cell_Name = input('>> Cell number (scan barcode)')
    return cell_Name





def readscale():
    mass = scaletest.read(scaletest.tare)
    scaletest.refreshscale()
def tarescale():
    scaletest.tare = scaletest.tare()
    scaletest.refreshscale()
def refreshscale():
    massvallbl.configure(
        text = mass
    )
    IDnum.configure(
        text = cell_Name
    )






'''
scan cell
measure mass
load into holder
press start
take impedence and submit
test will start after submission and LED will turn on
'''


def starttest1():
    cell_Dict = {}
    battery = 1
    BTM.battery_selection(battery)
    cell_Num = scan_cell()
    cell_Dict = {'Cell Number' : cell_Num}
    ID2num.update(text = cell_Num)
    
    # check that the battery has not already been tested
    if check_Name(cell_Num) is True:
        analogimpedence = simpledialog.askfloat("Analog Impedence","Measure Impedence using handheld device: Test will start once impedence is submitted",parent = window, minvalue = 0, maxvalue = 100)
        cell_Dict['Analog Impedence'] = analogimpedence
        BTM.start_test_LED(battery)
        Voc = BTM.meas_VOC()
        print("Voc: ",Voc)
        cell_Dict['Voc (V)'] = Voc
        impedance = BTM.dc_Impedance()
        print("impedance: ",impedance)
        cell_Dict['DC Impedance (Ohms)'] = impedance
        voltage_list,time_list = BTM.ratio_Capacity_BK8502()
        print(voltage_list, " ", time_list)
        cell_Dict.update({'Capacity Time': time_list, 'Capacity Voltage': voltage_list})
    
        df_battery_dict = pd.DataFrame({key: pd.Series(value) for key, value in cell_Dict.items()})
        df_battery_dict.to_excel(fileFolder + '/Test cell ' + cell_Dict['Cell Number'] + '.xlsx')
    
        BTM.finish_test_LED(battery)
        ID2num.update(text = "---") 
    else:
        print("Battery already tested")
        # add a pop up
        

def starttest2():
    cell_Dict = {}
    battery = 1
    
    BTM.battery_selection(battery)
    cell_Num = scan_cell()
    cell_Dict = {'Cell Number' : cell_Num}
    ID2num.update(text = cell_Num)
    
    # check that the battery has not already been tested
    if check_Name(cell_Num) is True:
        analogimpedence = simpledialmg.askfloat("Analog Impedence","Measure Impedence using handheld device",parent = window, minvalue = 0, maxvalue = 100)
        cell_Dict['Analog Impedence'] = analogimpedence
        BTM.start_test_LED(battery)
        Voc = BTM.meas_VOC()
        print("Voc: ",Voc)
        cell_Dict['Voc (V)'] = Voc
        impedance = BTM.dc_Impedance()
        print("impedance: ",impedance)
        cell_Dict['DC Impedance (Ohms)'] = impedance
        voltage_list,time_list = BTM.ratio_Capacity_BK8502()
        print(voltage_list, " ", time_list)
        cell_Dict.update({'Capacity Time': time_list, 'Capacity Voltage': voltage_list})
    
        df_battery_dict = pd.DataFrame({key: pd.Series(value) for key, value in cell_Dict.items()})
        df_battery_dict.to_excel(fileFolder + '/Test cell ' + cell_Dict['Cell Number'] + '.xlsx')
    
        BTM.finish_test_LED(battery)
        ID2num.update(text = "---")
      else:
        print("Battery already tested")
        # add a pop up      



# this function checks to see if there is already a document with the same name +> cell aready tested
# returns True or False
def check_Name(cell_Num):
        fileNames = os.listdir(fileFolder)
        full_cell_name = 'Test cell ' + cell_Num + '.xlsx'
        bool_Val = full_cell_name in fileNames
        return bool_Val





window = tk.Tk()
window.title("21700 Battery Profile")
window.geometry("1200x700")
window.resizable(0,0)
window.grid_rowconfigure(1,weight = 1)
window.grid_columnconfigure(2,weight = 1)




#title frame
titleframe = tk.Frame(window,
    width = 1200,
    height = 100,
    borderwidth=2,
    relief = SUNKEN
)
titleframe.grid(row = 1, column = 1, sticky = N, pady = 0, padx = 0)
titleframe.place(width = 1200, height = 100)

#3 columns
scaleframe = tk.Frame(window,
    width = 400,
    height = 800,
    borderwidth=2,
    relief = SUNKEN
)
scaleframe.grid(row = 1, column = 1,sticky = NS, pady = 0, padx = 0)
scaleframe.place(x = 0, y = 100, width = 400,height = 600)


site1frame = tk.Frame(window,
    width = 400,
    height = 800,
    borderwidth=2,
    relief = SUNKEN
)
site1frame.grid(row = 1, column = 2,sticky = NS,pady = 0, padx = 0)
site1frame.place(x=400, y = 100, width = 400,height = 600)


site2frame = tk.Frame(window,
    width = 400,
    height = 800,
    borderwidth=2,
    relief = SUNKEN
)
site2frame.grid(row = 1, column = 3,sticky = NS, pady = 0, padx = 0)
site2frame.place(x=800, y = 100, width = 400,height = 600)




#title##########################################
titlelbl = tk.Label(
    titleframe,
    text = "21700 Battery Testing",
    anchor = CENTER,
    font = ('Arial',35)
)
titlelbl.place(y = 20, width = 1200)







#scale #########################################

scalelbl = tk.Label(
    scaleframe,
    text = "Scale",
    font=("Arial",30)
    )
scalelbl.grid(row = 1, sticky = N)
scalelbl.place(width = 390)

ID1lbl = tk.Label(
    scaleframe,
    text = "ID"
    )
ID1lbl.grid(row = 2)
ID1lbl.place(y=60,width = 390)

IDnum = tk.Label(
    scaleframe,
    # text = config.IDscale
)
IDnum.grid(row = 3)
IDnum.place(y=100, width = 390)

tarebtn = tk.Button(
    scaleframe,
    text = "Tare",
    height = 5,
    command = tarescale
    )
tarebtn.grid(row = 4)
tarebtn.place(x=25,y = 150,width = 350,height = 100)

readbtn = tk.Button(
    scaleframe,
    text = "Read",
    height = 5,
    command = readscale
)
readbtn.grid(row = 5)
readbtn.place(x = 25,y=250,width = 350, height = 100)


readvallbl = tk.Label(
    scaleframe,
    text = mass
    )
readvallbl.grid(row = 6)
readvallbl.place(y = 350, width = 390, height = 50)

massvallbl = tk.Label(
    scaleframe,
    text = "-----"
)
massvallbl.grid(row = 7)
massvallbl.place(y=400,width = 390,height = 50)

#scale #########################################

#site 1#########################################
site1lbl = tk.Label(
    site1frame,
    text = "Site 1",
    font = ("Arial",30)
    )
site1lbl.grid(row = 1, sticky = N)
site1lbl.place(width = 390)

ID2lbl = tk.Label(
    site1frame,
    text = "ID"
)
ID2lbl.grid(row = 2)
ID2lbl.place(y=60,width = 390)

ID2num = tk.Label(
    site1frame,
    text = cell_Name
)
ID2num.grid(row = 3)
ID2num.place(y=100, width = 390)


data1lbl = tk.Label(
    site1frame,
    text = "Mass: \n\nOpen Circuit Volatage: \n\nDC Internal Resistance: \n\nAC Internal Resistance: \n\nCapacity Ratio: ",
    justify=LEFT
)
data1lbl.grid(row = 3)
data1lbl.place(y=150,x=50, width = 200)

start1btn = tk.Button(
    site1frame,
    text = "Start",
    bg = '#8dc989',
    command = starttest1
)
start1btn.grid(row = 5)
start1btn.place(y= 400,x=25,width = 350, height = 50)

errorlbl = Label(
    site1frame,

    )
errorlbl.grid(row = 6)
errorlbl.place(y=500, width = 390)

#site 1#########################################

#site 2#########################################

site2lbl = tk.Label(
    site2frame,
    text = "Site 2",
    font = ("Arial",30)
    )
site2lbl.grid(row = 1, sticky = N)
site2lbl.place(width = 390)

ID3lbl = tk.Label(
    site2frame,
    text = "ID:"
)
ID3lbl.grid(row = 2)
ID3lbl.place(y=60,width = 390)

ID3num = tk.Label(
    site2frame,
    text = cell_Name
)
ID3num.grid(row = 3)
ID3num.place(y=100, width = 390)

data2lbl = tk.Label(
    site2frame,
    text = "Mass: \n\nOpen Circuit Volatage: \n\nDC Internal Resistance: \n\nAC Internal Resistance: \n\nCapacity Ratio: ",
    justify=LEFT
)
data2lbl.grid(row = 3)
data2lbl.place(y=150,x=50, width = 200)

start2btn = tk.Button(
    site2frame,
    text = "Start",
    bg = '#8dc989',
    command = starttest2
)
start2btn.grid(row = 5)
start2btn.place(y= 400,x=25,width = 350, height = 50)


errorlbl2 = Label(
    site2frame,

    )
errorlbl2.grid(row = 6)
errorlbl2.place(y=500, width = 390)

#site 2#########################################







window.mainloop()








