from collections import namedtuple
#from distutils.log import error
from tkinter import *
import tkinter as tk
from tkinter.constants import *
from tkinter.ttk import Labelframe


#from matplotlib import scale
import tkcommands as tkcommands
from tkcommands import starttest
import config











 
config.initialize()
errorstate = config.msgsite1
errorstate2 = config.msgsite2







def errorlblupdate():
    tkcommands.starttest()
    refresh(errorlbl)
    

def errorlbl2update():
    tkcommands.starttest()
    refresh2(errorlbl2)

def refresh(x):
    x.configure(
        text = config.msgsite1
    )
def refresh2(x):
        x.configure(
        text = config.msgsite2
    )








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
    text = "----"
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
    command = errorlblupdate
)
start1btn.grid(row = 5)
start1btn.place(y= 400,x=25,width = 150, height = 50)

remove1btn = tk.Button(
    site1frame,
    text = "Remove",
    bg = '#ab5454'
)
remove1btn.grid(row = 5)
remove1btn.place(y = 400,x=225,width = 150,height = 50)

errorlbl = Label(
    site1frame,
    text = errorstate
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
    text = "----"
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
    command = errorlbl2update
)
start2btn.grid(row = 5)
start2btn.place(y= 400,x=25,width = 150, height = 50)

remove2btn = tk.Button(
    site2frame,
    text = "Remove",
    bg = '#ab5454'
)
remove2btn.grid(row = 5)
remove2btn.place(y = 400,x=225,width = 150,height = 50)

errorlbl2 = Label(
    site2frame,
    text = errorstate2
    )
errorlbl2.grid(row = 6)
errorlbl2.place(y=500, width = 390)

#site 2#########################################







window.mainloop()








