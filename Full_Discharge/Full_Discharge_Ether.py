## This script is to be ran for each cell to be tested
## Tests: Voc, Impedance, FULL Capacity Discharge

import pyvisa
import socket
import serial
import time
import pyfirmata
import time
import threading
import pandas as pd
import numpy as np
from scipy.stats import linregress
from statistics import mean

import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 2000  # Set Duration To 1000 ms == 1 second


### User INPUT ###
fileFolder = 'C:/Users/nwoodwa/Desktop/SolarPack/'

### End of User Input ###

# a Keithley 2450 SourceMeter is used for the open voltage reading, voltage reading during discharge,
# and both the source and meter for impedence testing
# connect to Kiethley via ethernet
#IP adress of keithly


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





#initialize connection and reset
TCP_IP = "169.254.246.87"
TCP_Port = 5025
keithley = socket.socket()
keithley.connect((TCP_IP, TCP_Port))
keithley.send("*RST")
print("ID: ", query_Keithley("*IDN?"))

send_Keithley('OUTP:SMOD HIMP')  # turn on high-impedance output mode; so battery wont drain while just sitting




# Connect to Arduino
# sets serial connection with arduino uno and establish pin connections
# arduinoPort = 'COM4'
# arduinoB = pyfirmata.Arduino(arduinoPort)  # arduino uno #if MEGA then use ArduinoMega(arduinoPort)
# it = pyfirmata.util.Iterator(arduinoB)
# it.start()
# bk_GND = arduinoB.get_pin('d:2:o')  # for relay
# bk_POS = arduinoB.get_pin('d:3:o')  # for relay
# ensures both relays are off; set to NC position
# bk_GND.write(1)
# bk_POS.write(1)

### Setup V 0.1
## write gpio pin
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.board)
# relays = {'bk_POS': 17, 'bk_GND': 18}
# for key, value in relays():     # loop to set up each relay pin to output 
#    GPIO.setup(value, GPIO.OUT)      # GPIO.setup(17, GPIO.OUT)
# ensures both relays are off; set to NC position
# GPIO.output(relays['bk_POS'], 1)
# GPIO.output(relays['bk_GND'], 1)


### Setup V 0.2
# BK 8502 DC Load Supply is used for to discharge the cells at 10A
# a relay is used to turn on/off the load supply connection
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)


# Relay k16: POS; NC =  battery 1, NO = nothing (battery 2)         # Battery_POS
# Relay k15: NEG; NC =  battery 1, NO = nothing (battery 2)         # Battery_NEG

# Relay k3: NEG; NC =  battery 1, NO = nothing (battery 2)          # Force_NEG
# Relay k4: POS; NC =  battery 1, NO = nothing (battery 2)          # Force_POS

# Relay k1: POS; NC = Keithely Sense; NO = BK Load                  # Sense_BK_POS
# Relay k2: NEG; NC = Keithely Sense; NO = BK Load                  # Sense_BK_NEG


# Relay k13: LED ground; NC = nothing, NO = Battery 1 indicator     # LED_1
# Relay k14: LED ground; NC = nothing, NO = Battery 2 indicator     # LED_2



relays = {'Battery_POS': 13, 'Battery_NEG': 15, 'Sense_BK_POS': 3, 'Sense_BK_NEG': 5, 'Force_NEG': 7, 'Force_POS': 11, 'LED_1': 19, 'LED_2': 21}


# Battery 1 = Normally closed position
GPIO.output(relays['Battery_POS'], 0)   # relays off to NC position
GPIO.output(relays['Battery_NEG'], 0)      
GPIO.output(relays['Force_NEG'], 0)  



# loop to set up each relay pin to output
# set all to NC postion
for value in relays.values():
   GPIO.setup(value, GPIO.OUT)      # GPIO.setup(17, GPIO.OUT)
   GPIO.output(value, 1)

## Set relays to battery 1
GPIO.output(relays['Battery_POS'], 1)   # relays to NC position
GPIO.output(relays['Battery_NEG'], 1)
GPIO.output(relays['Force_NEG'], 1)


cell_Dict = {}

# function to save the dataframe
# function to be called after test 1 and 2, and every 5 minutes during capasicty discharge test 3
def save_DF():
    # turn dictionary to dataframe
    # uses series so columns can be of differnt length

    df_battery_dict = pd.DataFrame({key: pd.Series(value) for key, value in cell_Dict.items()})
    df_battery_dict.to_excel(fileFolder + 'Test cell ' + cell_Dict['Cell Number'] + '.xlsx')

def set_forVoltageReading():
    send_Keithley('SOUR:VOLT:RANG 20')

def voltage_Reading():
    send_Keithley('OUTP ON')
    time.sleep(.2)

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

print('Ensure proper connection and equipment is turned on')
cell_Name = input('>> Cell number (scan barcode)')
cell_Dict = {'Cell Number': cell_Name}

input('Press Enter to start testing >> ')

# # Test 1
# print('Measure AC Impedance using handhgeld tool')
# cell_AC_Impd = input('>> AC Impedance (milli-Ohm')
# cell_Dict = {'Cell AC Impedance': cell_AC_Impd}
#

# Test 2
print('   Starting Measuring Voc...')

# set relay to sense 
GPIO.output(relays['Sense_BK_POS'], 0)      # relays off to NC = sense 
GPIO.output(relays['Sense_BK_NEG'], 0)   

set_forVoltageReading()

# loop 10 times and compute the average Voc at a discharge of 0.1A
vocL = []
for i in range(5):
    volt = voltage_Reading()
    # print(volt)

    vocL.append(volt)


Voc = mean(vocL)
cell_Dict['Voc (V)'] = Voc
print("      Voc is {:.2f}".format(Voc))


# Test 3
print("   Starting Measuring DC Impedance...")

# set relay to sense
GPIO.output(relays['Sense_BK_POS'], 1)      # relays off to NC = sense
GPIO.output(relays['Sense_BK_NEG'], 1)

# set KEITHLEY settings
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

cell_Dict['DC Impedance (Ohms)'] = impedance
print('      Impedance is {:.1f} m-Ohm'.format(impedance))


# Test 4
print("   Starting Measuring Total Discharge...")

send_Keithley('*RST')  # first line is to reset the instrument # 2-Wire mode by default
set_forVoltageReading()

iteration = 1  # iteration must start at 1 for Keithly write
voltLimit = 2.75  # voltage which to stop the test
voltageL = []  # list of voltage readings
measTimeL = []  # list of times of readings

rollingList = []  # list of voltage rolling  averaging for determinging when we reach the end test voltLimit; helps to ignore random drops/spikes

# set relay to BK Load
GPIO.output(relays['Sense_BK_POS'], 0)      # relays ib to NO = BK Load
GPIO.output(relays['Sense_BK_NEG'], 0)
time.sleep(1)
startTime = time.time()

while iteration >= 0:  # infinite while loop; breaks when voltLimit is reached
    # print(iteration)

    voltage = voltage_Reading()
    print(voltage)
    voltageL.append(float(voltage))

    time_measure = time.time() - startTime
    measTimeL.append(float(time_measure))

    # takes the rolling average voltage
    # this average is used to determine when to break from the tests
    rollingList.append(float(voltage))
    if len(rollingList) > 15:
        rollingList.pop(0)  # removes the very first item in list when there are 10 measurements

        if mean(rollingList) <= voltLimit:  # <= voltLimit for Discharging # >= voltLimit for Charging
            # print('break')
            break  # breaks out of while loop when the specified condition is met
    iteration += 1


    time.sleep(1)


    cell_Dict.update({'Capacity Time': measTimeL, 'Capacity Voltage': voltageL})

    # saves data every 150 seconds => 15 iterations
    if iteration % 15:
        tSave = threading.Thread(target=save_DF)
        tSave.start()




# set relay back to sense 
GPIO.output(relays['Sense_BK_POS'], 1)      # relays off to NC = sense
GPIO.output(relays['Sense_BK_NEG'], 1)

save_DF()
print("TURN OFF BK 8502")
print("Testing Complete")
winsound.Beep(frequency, duration)
