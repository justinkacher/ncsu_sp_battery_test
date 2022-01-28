from collections import namedtuple
from tkinter import *
import tkinter as tk
from tkinter.constants import *
from tkinter.ttk import Labelframe

#number of batteries to test
numbatteries = 12


window = tk.Tk()
window.title("18650 Battery Profile")
window.geometry("1200x800")


#3 columns
scaleframe = tk.Frame(window,
    borderwidth=5,
    relief = GROOVE,
    
)
scaleframe.grid(column = 1,row = 1)
site1frame = tk.Frame(window,
    borderwidth=5,
    relief = GROOVE
)
site1frame.grid(column = 2,row = 1)
site2frame = tk.Frame(window,
    borderwidth=5,
    relief = GROOVE
)
site2frame.grid(column = 3,row = 1)


#scale #########################################

scalelbl = tk.Label(
    scaleframe,
    text = "Scale"
    )
scalelbl.grid(row = 0)

ID1lbl = tk.Label(
    scaleframe,
    text = "ID: "
    )
ID1lbl.grid(row = 1)

tarebtn = tk.Button(
    scaleframe,
    text = "Tare",
    width = 30,
    height = 5
    )
tarebtn.grid(row = 2)

readbtn = tk.Button(
    scaleframe,
    text = "Read",
    width = 30,
    height = 5
)
readbtn.grid(row = 3)

masslbl = tk.Label(
    scaleframe,
    text = "Read Value:"
    )
masslbl.grid(row = 4)

#scale #########################################

#site 1#########################################
site1lbl = tk.Label(site1frame,
    text = "Site 1"
    )
site1lbl.grid(row = 1,columnspan=2)

ID2lbl = tk.Label(site1frame,
    text = "ID:"
)
ID2lbl.grid(row = 2,columnspan=2)

data1lbl = tk.Label(site1frame,
    text = "Mass: \nOpen Circuit Volatage: \nDC Internal Resistance: \nAC Internal Resistance: \nCapacity Ratio: "
)
data1lbl.grid(row = 3,columnspan=2)

start1btn = tk.Button(site1frame,
    text = "Start"
)
start1btn.grid(row = 4, column = 1)

remove1btn = tk.Button(site1frame,
    text = "Remove"
)
remove1btn.grid(row = 4, column = 2)

#site 1#########################################

#site 2#########################################

site2lbl = tk.Label(site2frame,
    text = "Site 2"
    )
site2lbl.grid(row = 1,columnspan=2)

ID3lbl = tk.Label(site2frame,
    text = "ID:"
)
ID3lbl.grid(row = 2,columnspan=2)

data2lbl = tk.Label(site2frame,
    text = "Mass: \nOpen Circuit Volatage: \nDC Internal Resistance: \nAC Internal Resistance: \nCapacity Ratio: "
)
data2lbl.grid(row = 3,columnspan=2)

start2btn = tk.Button(site2frame,
    text = "Start"
)
start2btn.grid(row = 4, column = 1)

remove2btn = tk.Button(site2frame,
    text = "Remove"
)
remove2btn.grid(row = 4, column = 2)

#site 2#########################################












window.mainloop()