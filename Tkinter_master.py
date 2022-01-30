from collections import namedtuple
from tkinter import *
import tkinter as tk
from tkinter.constants import *
from tkinter.ttk import Labelframe

from matplotlib import scale

#number of batteries to test
numbatteries = 12


window = tk.Tk()
window.title("18650 Battery Profile")
window.geometry("1200x600")
window.resizable(0,0)
window.grid_rowconfigure(1,weight = 1)
window.grid_columnconfigure(2,weight = 1)


#3 columns
scaleframe = tk.Frame(window,
    width = 400,
    height = 800,
    borderwidth=5,
    relief = GROOVE
)
scaleframe.grid(row = 1, column = 1,sticky = NS, pady = 0, padx = 0)
scaleframe.place(width = 400,height = 800)
#scaleframe.pack(side = LEFT)
#scaleframe.place(
#    anchor='c',
#    relx = 1/6,
#    rely = 1/2
#)
site1frame = tk.Frame(window,
    width = 400,
    height = 800,
    borderwidth=5,
    relief = GROOVE
)
site1frame.grid(row = 1, column = 2,sticky = NS,pady = 0, padx = 0)
site1frame.place(x=400,width = 400,height = 800)
#site1frame.pack()
#site1frame.place(
#    anchor='c',
#    relx = 3/6,
#    rely = 1/2
#)
site2frame = tk.Frame(window,
    width = 400,
    height = 800,
    borderwidth=5,
    relief = GROOVE
)
site2frame.grid(row = 1, column = 3,sticky = NS, pady = 0, padx = 0)
site2frame.place(x=800,width = 400,height = 800)
#site2frame.pack(side = RIGHT)
#site2frame.place(
#    anchor='c',
#    relx = 5/6,
#    rely = 1/2
#)


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
    text = "----"
)
IDnum.grid(row = 3)
IDnum.place(y=100, width = 390)

tarebtn = tk.Button(
    scaleframe,
    text = "Tare",
    height = 5
    )
tarebtn.grid(row = 4)
tarebtn.place(x=25,y = 150,width = 350,height = 100)

readbtn = tk.Button(
    scaleframe,
    text = "Read",
    height = 5
)
readbtn.grid(row = 5)
readbtn.place(x = 25,y=250,width = 350, height = 100)


readvallbl = tk.Label(
    scaleframe,
    text = "Read Value"
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