from tkinter import *
import tkinter as tk

#from mass.hx711_as_tkinter import *


#hx711 libraries
from tkinter.constants import *
#from mass.RaspberryPi_Read import *
#from hx711 import HX711                 #library will not import properly when not on Raspberry Pi
#import RPi.GPIO as GPIO                 #library will not import properly when not on Raspberry pi
#rpi read libraries
#import RPi.GPIO as GPIO


#from matplotlib.pyplot import gray

window = tk.Tk()
window.title("18650 Battery Profile")



'''
top test progress bar
- to do - color to green when test is active
- to do - color to red if test is flagged as incorrect and set to re perform
'''


#Setup Page --------------------------------------------------------------

setupframe = Frame(window)
setupframe.pack(side = BOTTOM)

#Setup Page --------------------------------------------------------------

#progress bar -------------------------------------------------------------
progframe = Frame(window)
progframe.pack(side = TOP)


toplblmass = tk.Label(
    progframe,
    text = "Mass",
    padx = 10,
    bg = "gray"
    )
toplblocv = tk.Label(
    progframe,
    text = "Open Circuit Voltage",
    padx = 10,
    bg = "gray"
    )
toplbldcir = tk.Label(
    progframe,
    text = "DC Internal resistance",
    padx = 10,
    bg = "gray"
    )
toplblacir = tk.Label(
    progframe,
    text = "AC Internal resistance",
    padx = 10,
    bg = "gray"
    )
toplblcaprat = tk.Label(
    progframe,
    text = "Capacity Ratio",
    padx = 10,
    bg = "gray"
    )


toplblmass.pack(side = LEFT)
toplblocv.pack(side = LEFT)
toplbldcir.pack(side = RIGHT)
toplblacir.pack(side = RIGHT)
toplblcaprat.pack(side = RIGHT)

#progress bar -------------------------------------------------------------





#mass page ----------------------------------------------------------------
massframe = Frame(window)

#frame creation ##########################
def showmassframe():
    massframe.pack(side = BOTTOM)
    toplblmass.config(
        bg = "green"
    )

    
    Lframe = Frame(massframe)
    Lframe.pack(side = LEFT)

    rightoutputframe = Frame(massframe)
    rightoutputframe.pack(  
            side = RIGHT,
            padx = 20
        )

    topRframe = Frame(rightoutputframe)
    topRframe.pack(side = TOP)

    midRframe = Frame(rightoutputframe)
    midRframe.pack()

    botRframe = Frame(rightoutputframe)
    botRframe.pack(
            side = BOTTOM,
            pady = 10
            )
    ##########################################


    #Tare Button
    print("generating tare button")
    tarebutton = tk.Button(
            Lframe,
            text="Tare",
            height = 10,
            width = 20,
            font = ("Courier",10),
            #command = fcntare
        )
    tarebutton.pack(side = TOP)
    print("pack")

    #TAKE MEASURE BUTTON
    print("generating measure btn")
    measurebutton = tk.Button(
            Lframe,
            text="Take Measurement",
            height = 10,
            width = 20,
            font = ("Courier",10),
            #command = fmeasure
        )
    measurebutton.pack(side = BOTTOM)
    print("Done")

    #SAVE VALUE LABEL
    print("generating save lbl")
    checkvallbl = tk.LabelFrame(
            topRframe,
            text = "Save this value?",
            height = 20,
            width=20,
            font = ("Courier",10)
        )
    checkvallbl.pack()
    print("Done")

    #VALUE OF MEASURE LABEL
    print("generating val lbl")
    measurevallbl = tk.Label(
            checkvallbl,
            text = "measureval",
            font = ("Courier",40)
        )
    measurevallbl.pack()
    print("Done")
'''
    #YES BUTTON
    print("generating 'yes' button")
    yesbtn = tk.Button(
            botRframe,
            text = "YES",
            height=3,
            width=10,
            font = ("Courier",10)
        )
    yesbtn.pack(side = LEFT)
    print("Done")

    #NO BUTTON
    print("generating 'no' button")
    nobtn = tk.Button(
            botRframe,
            text = "NO",
            height=3,
            width=10,
            font = ("Courier",10)
        )
    nobtn.pack(side = RIGHT)
    print("Done")
'''
def hidemassframe():
    toplblmass.config(bg = "gray")
    massframe.pack_forget()

#end mass page ----------------------------------------------------------------


#open circuit voltage -----------------------------------------------------
ocvframe = Frame(window)
def showocv():
    ocvframe.pack(side = BOTTOM)
    toplblocv.config(bg = "green")

#open circuit voltage -----------------------------------------------------


#DC internal resistance ---------------------------------------------------

#DC internal resistance ---------------------------------------------------


#AC internal resistance ---------------------------------------------------

#AC internal resistance ---------------------------------------------------

#Capacity Ratio -----------------------------------------------------------

#Capacity Ratio -----------------------------------------------------------





#window.show_frame(progframe)
if input('mass? y/n') == 'y':
    showmassframe()
if input('y/n') == 'n':
    hidemassframe()


window.mainloop()