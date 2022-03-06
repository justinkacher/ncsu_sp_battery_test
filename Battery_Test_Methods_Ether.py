import pyvisa
import time
import pandas as pd
import numpy as np
from scipy.stats import linregress
from statistics import mean
import socket
import time
import RPi.GPIO


#IP adress of keithly
TCP_IP = ""
TCP_Port = 

#send commands to keithley via socket
def send_Keithley(command):
    command += "\n"
    keithley.send(command.encode())
    return

def recieve_Keithley():
    return keithley.recv(1024).decode()


def query_Keithley(command):
    send_Keithley(command)
    return recieve_Keithley()










# a Keithley 2450 SourceMeter is used for the open voltage reading, voltage reading during discharge,
# and both the source and meter for impedence testing
#initialize connection and reset
initialize connection and reset
TCP_IP = "169.254.246.87"
TCP_Port = 5025
keithley = socket.socket()
keithley.connect((TCP_IP, TCP_Port))
keithley.send("*RST")
print("ID: ", query_Keithley("*IDN?"))
send_Keithley('OUTP:SMOD HIMP')  # turn on high-impedance output mode; so battery wont drain while just sitting


# BK 8502 DC Load Supply is used for to discharge the cells at 10A
# a relay is used to turn on/off the load supply connection
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.board)
GPIO.setup(17, GPIO.OUT)

# Relay k16: POS; NC =  battery 1, NO = nothing (battery 2)         # Battery_POS
# Relay k15: NEG; NC =  battery 1, NO = nothing (battery 2)         # Battery_NEG

# Relay k3: NEG; NC =  battery 1, NO = nothing (battery 2)          # Force_NEG
# Relay k4: POS; NC =  battery 1, NO = nothing (battery 2)          # Force_POS

# Relay k1: POS; NC = Keithely Sense; NO = BK Load                  # Sense_BK_POS
# Relay k2: NEG; NC = Keithely Sense; NO = BK Load                  # Sense_BK_NEG


# Relay k13: LED ground; NC = nothing, NO = Battery 1 indicator     # LED_1
# Relay k14: LED ground; NC = nothing, NO = Battery 2 indicator     # LED_2



relays = {'Battery_POS': 13, 'Battery_NEG': 15, 'Sense_BK_POS': 3, 'Sense_BK_NEG': 5, 'Force_NEG': 7, 'Force_POS': 11, 'LED_1': 19, 'LED_2': 21}

# loop to set up each relay pin to output 
for key, value in relays():
   GPIO.setup(value, GPIO.OUT)      # GPIO.setup(17, GPIO.OUT)


# turn ON LED for which battery is being tested
def start_test_LED(battery):
    if battery is 1:
        GPIO.output(relays['LED_1'], 1)      # LED 1 = k13 # relays on to NO positions
    if battery is 2:
        GPIO.output(relays['LED_2'], 1)      # LED 2 = k14 # relays on to NO positions

# turn OFF LED for which battery is being tested
def finish_test_LED(battery):
    if battery is 1:
        GPIO.output(relays['LED_1'],0)      # LED 1 = k13 # relays off to NC positions
    if battery is 2:
        GPIO.output(relays['LED_2'], 0)      # LED 2 = k14 # relays off to NC positions


def battery_selection(battery):
    if battery is 1:
        GPIO.output(relays['Battery_POS'], 0)   # relays off to NC position
        GPIO.output(relays['Battery_NEG'], 0)      
        GPIO.output(relays['Force_NEG'], 0)  
    if battery is 2:
        GPIO.output(relays['Battery_POS'], 1)   # relays on to NO position
        GPIO.output(relays['Battery_NEG'], 1) 
        GPIO.output(relays['Force_POS'], 0)


def set_forVoltageReading():
    send_Keithley('SOUR:VOLT:RANG 20')

def voltage_Reading():
    send_Keithley('OUTP ON')
    time.sleep(.15)

    voltReading = query_Keithley('MEAS:VOLT? "defbuffer1", READ')
    send_Keithley('OUTP OFF')

    # voltR = float(voltReading)
    # print(voltR)
    return float(voltReading)

# function takes current source limit
def SMU(sourceLimit):
    send_Keithley(f'SOUR:VOLT:ILIM {sourceLimit}')  # set voltage source (current) limit
    current = query_Keithley('READ? "defbuffer1"')
    volt = query_Keithley('READ? "defbuffer1", SOUR')   # a ? is used for a query command otherwise is a set command
                                                        # defbuffer1 returns sense value

    return current, volt


## Open Circuit Voltage
# returns open circuit voltage measurement    

# battery connection:
# Sense Hi connect to positive terminal
# Sense Lo connect to negative terminal
def meas_VOC():
    
    # set kethley settings
    set_forVoltageReading()
    
    # set relay to sense 
    GPIO.output(relays['Sense_BK_POS'], 0)      # relays off to NC = sense 
    GPIO.output(relays['Sense_BK_NEG'], 0)      


    # loop 5 times and compute the average Voc
    vocL = []
    for i in range(5):
        volt = voltage_Reading()
        vocL.append(volt)
        # print(volt)
        
    
    Voc = mean(vocL)

    return Voc


##  DC Internal Resistance (DC Impedance Test)
# Returns DC Impedance
    
# Apply linear sweep DC current and measure voltage = resistance
# (V2-V1)/(I2-I1) = DC internal resistance
# current sweep: current limit is linearly changed and voltage response is observed, giving the resistance as the slope of the lined
# Kiethley: set voltage source to discharge or charge and ues current limit to set the constant current level
    
# battery connection Keithley:
# four sense probe. Keithley measure current in terms of ohm
# Sense Hi and Force Hi connect to positive terminal
# Sense Lo and Force Lo connect to negative terminal
def dc_Impedance():

    # set relay to sense 
    GPIO.output(relays['Sense_BK_POS'], 0)      # relays off to NC = sense 
    GPIO.output(relays['Sense_BK_NEG'], 0)      
    
    sourceVoltage = 2.65  # Charging: VSource > VBattery; Discharging: VS < VB # 18650 is 3.7v; max charging is 4.2v and min discharge final is 2.75
    voltageRange = 20  # 20mV, 200mV, 2V, 20V, 200V
    sourceLimit = np.linspace(0.1, 1, 10)     # returns array; start value, end value, number of points
    
    currentRange = 1.05  # Max 1.05A
    
    send_Keithley('*RST')  # first line is to reset the instrument
    send_Keithley('OUTP:SMOD HIMP')  # turn on high-impedance output mode
    send_Keithley('SENS:CURR:RSEN ON')  # set to 4-wire sense mode  # OFF = 2-Wire mode
    send_Keithley('SENS:FUNC "CURR"')  # set measure, sense, to current
    send_Keithley(f'SENS:CURR:RANG {currentRange}')  # set current range # can also be 'SENS:CURR:RANG:AUTO ON'
    send_Keithley('SENS:CURR:UNIT AMP')  # set measure units to Ohm, can also be Watt or Amp
    send_Keithley('SOUR:FUNC VOLT')  # set source to voltage
    send_Keithley(f'SOUR:VOLT {sourceVoltage}')  # set output voltage => discharge or charge test
    send_Keithley('SOUR:VOLT:READ:BACK ON')  # turn on source read back
    send_Keithley(f'SOUR:VOLT:RANG {voltageRange}')  # set source range
    send_Keithley(f'SOUR:VOLT:ILIM {sourceLimit[0]}')  # set source (current) limit
    send_Keithley('OUTP ON')  # turn on output, source
    
    # loop 10 times to and return the average DC impedance
    currentL_impedance = []
    voltL_impedance = []
    for i in range(len(sourceLimit)):
        send_Keithley(f'SOUR:VOLT:ILIM {sourceLimit[i]}')  # set source (current) limit
        time.sleep(0.1)
    
        curr = query_Keithley('READ? "defbuffer1"')
        currentL_impedance.append(float(curr))
    
        volt =query_Keithley('READ? "defbuffer1", SOUR')  # a ? is used for a query command otherwise is a set command
                                                          # defbuffer1 returns sense value
        voltL_impedance.append(volt)
    
    send_Keithley('OUTP OFF')  # turn off keithley
    
    impedanceL = []
    for i in range(len(voltL_impedance)-1):
        DC_impedance = (voltL_impedance[i] - voltL_impedance[i+1]) / (currentL_impedance[i] - currentL_impedance[i+1])
        # print(DC_impedance)
        impedanceL.append(DC_impedance)
    
    impedance_Avg = mean(impedanceL)
    # print('current')
    # print(currentL_impedance)
    # print(' volt')
    # print(voltL_impedance)
    
    impedance = impedance_Avg*1000   # to get to milli- Ohms

    return impedance



## Ratio Capacity Test
# returns list of voltage and times    

# Takes voltage discharge for 30 seconds
# Comapare to baseline of full capacity cells by impedence

# returns lists of currentL, voltageL , measTimeL
def ratio_Capacity_BK8502(battery):


    send('*RST')                              # first line is to reset the instrument
    send('OUTP:SMOD HIMP')                    # turn on high-impedance output mode
#    send('SENS:CURR:RSEN OFF')                # set to 4-wire sense mode  # OFF = 2-Wire mode # by default?
    send('SENS:FUNC "VOLT"')                  # set measure, sense, to current
    send('SENS:CURR:RANG:AUTO ON')            # set current range to auto

    stopTime = 30           # discharge for 30 seconds
    testTime = 0            # initiate testTime to zero seconds
    voltageL = []           # list of voltage readings
    measTimeL = []          # list of times of readings

    # set relay to BK Load
    GPIO.output(relays['Sense_BK_POS'], 1)      # relays ib to NO = BK Load 
    GPIO.output(relays['Sense_BK_NEG'], 1)   
    
    startTime = time.time()

    while testTime >= stopTime:    # loop until 30 seconds, stoptime has passed
        send('READ? "defbuffer1"')        # get voltage sense reading
        voltage = recieve()
        # print(voltage)
        voltageL.append(float(voltage))

        time = time.time() - startTime
        measTimeL.append(float(time))

        time.sleep(1)      # sleep is in seconds    # 1 second between measurements


    # turn relay to NC, thus DC Load is OFF
    # set relay back to sense 
    GPIO.output(relays['Sense_BK_POS'], 0)      # relays off to NC = sense 
    GPIO.output(relays['Sense_BK_NEG'], 0)   

    return currentL, voltageL, measTimeL
