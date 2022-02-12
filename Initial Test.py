## This script is to be ran for each cell to be tested
## Tests: Voc, Impedance, FULL Capacity Discharge

import pyvisa
import serial
import time
import pyfirmata
import time
import threading
import pandas as pd
import numpy as np
from scipy.stats import linregress
from statistics import mean


### User INPUT ###
fileFolder = 'C:/Users/nwoodwa/Desktop/SolarPack/'




### End of User Input ###

# a Keithley 2450 SourceMeter is used for the open voltage reading, voltage reading during discharge,
# and both the source and meter for impedence testing
# connect to Kiethley
rm = pyvisa.ResourceManager()
# print(rm.list_resources())     # returns a tuple of connected devices # 'USB0::0x05E6::0x2450::04366211::INSTR'
keithley = rm.open_resource('USB0::0x05E6::0x2450::04366211::INSTR')
# print(keithley.query("*IDN?"))      # query's the Identity of the device connected
keithley.write('*RST')


# Connect to Arduino
# sets serial connection with arduino uno and establish pin connections
arduinoPort = 'ttyo/USB0'
arduinoB = pyfirmata.Arduino(arduinoPort)         # arduino uno #if MEGA then use ArduinoMega(arduinoPort)
it = pyfirmata.util.Iterator(self.arduinoB)
it.start()
        # a: analog,  d: digital
        # i: input, o: output, s: servo, p: pwm
        # servo 0-180
        # pwm 0-255 or a float value 0 to 1.0
bk_GND = arduinoB.get_pin('d:2:o')         # for relay
bk_POS = arduinoB.get_pin('d:3:0')         # for relay
# ensures both relays are off; set to NC position
bk_GND.write(0)
bk_POS.write(0)

cell_Dict = {}

# function to save the dataframe
# function to be called after test 1 and 2, and every 5 minutes during capasicty discharge test 3
def save_DF():
        # turn dictionary to dataframe
    # uses series so columns can be of differnt length
    
    df_battery_dict = pd.DataFrame({key: pd.Series(value) for key, value in battery_dict.items()})
    df_battery_dict.to_excel(fileFolder+'Test cell ' + str(config.site1state) + '.xlsx')



print('Ensure proper connection and equipment is turned on')
cell_Name = input('>> Cell number: ')
cell_Dict = {'Cell number': cell_Name}


input('Press Enter to start testing >> ')


# Test 1
print('   Starting Test 1/3: Measuring Voc...')
keithley.write('*RST')                  # first line is to reset the instrument
keithley.write('SENS:CURR:RSEN OFF')    # OFF = 2-Wire mode #  set On for 4-wire sense mode
keithley.write('SENS:FUNC "VOLT"')      # set measure, sense, to voltage

# loop 10 times and compute the average Voc
vocL = []
for i in range(10):
    keithley.write('READ? "defbuffer1"')    # a ? is used for a query command otherwise is a set command
    voltage_i = keithley.read()               # defbuffer1 returns sense value
    vocL.append(voltage_i)
Voc = mean(vocL)
cell_Dict['Voc (V)'] = Voc
print("Voc is " + str(Voc))


# Test 2
print("   Starting Test 2/3: Measuring DC Impedance...")
sourceVoltage = 2.65          # Charging: VSource > VBattery; Discharging: VS < VB # 18650 is 3.7v; max charging is 4.2v and min discharge final is 2.75
voltageRange = 20            # 20mV, 200mV, 2V, 20V, 200V
sourceLimit = 1.05              # Current Limit = Charge or Discharge rate # units A => 460e-3 A =.46 A = 460mA
currentRange = 1             # Max 1.05A

keithley.write('*RST')      # first line is to reset the instrument
keithley.write('OUTP:SMOD HIMP')                    # turn on high-impedance output mode
keithley.write('SENS:CURR:RSEN ON')                 # set to 4-wire sense mode  # OFF = 2-Wire mode
keithley.write('SENS:FUNC "CURR"')                  # set measure, sense, to current
keithley.write(f'SENS:CURR:RANG {currentRange}')    # set current range # can also be 'SENS:CURR:RANG:AUTO ON'
keithley.write('SENS:CURR:UNIT OHM')               # set measure units to Ohm, can also be Watt or Amp
keithley.write('SOUR:FUNC VOLT')                    # set source to voltage
keithley.write(f'SOUR:VOLT {sourceVoltage}')        # set output voltage => discharge or charge test
keithley.write('SOUR:VOLT:READ:BACK ON')            # turn on source read back
keithley.write(f'SOUR:VOLT:RANG {voltageRange}')    # set source range
keithley.write(f'SOUR:VOLT:ILIM {sourceLimit}')     # set source (current) limit
keithley.write('OUTP ON')                           # turn on output, source

time.sleep(5)   # to let the battery reach a steady state discharge

# loop 10 times to and return the average DC impedance
impedanceL = []
for i in range(10):
    keithley.write('READ? "defbuffer1"')
    resistance = keithley.read()                         # units = Ohm
    # print(impedance)
    impedanceL.append(float(resistance))

keithley.write('OUTP OFF')      # turn keithley

impedance = mean(impedanceL)
cell_Dict['DC Impedance (Ohms)'] = impedance
print('Impedance is '+str(impedance))


# Test 3
print("Disconnect Keithley Force wires and connect BK 8502 DC Load & then turn on")
input("Press Enter to start test 3 >>")
print("   Starting Test 3/3: Measuring Total Discharge...")


keithley.write('*RST')                              # first line is to reset the instrument
keithley.write('OUTP:SMOD HIMP')                    # turn on high-impedance output mode
keithley.write('SENS:CURR:RSEN OFF')                # set to 4-wire sense mode  # OFF = 2-Wire mode # by default?
keithley.write('SENS:FUNC "VOLT"')                  # set measure, sense, to current
keithley.write('SENS:CURR:RANG:AUTO ON')            # set current range to auto

iteration = 1           # iteration must start at 1 for Keithly write
voltLimit = 2.75        # voltage which to stop the test
voltageL = []           # list of voltage readings
measTimeL = []          # list of times of readings

rollingList = []        # list of voltage rolling  averaging for determinging when we reach the end test voltLimit; helps to ignore random drops/spikes

# turn relay to NO, thus DC Load ON
bk_POS.write(1)
bk_GND.write(1)

startTime = time.time()

while iteration >= 0:    # infinite while loop; breaks when voltLimit is reached
    #print(iteration)

    keithley.write('READ? "defbuffer1"')
    voltage = keithley.read()
    # print(voltage)
    voltageL.append(float(voltage))

    time = time.time() - startTime
    measTimeL.append(float(time))


    # takes the rolling average voltage
    # this average is used to determine when to break from the tests
    rollingList.append(float(volt))
    if len(rollingList) > 15:
        rollingList.pop(0)              # removes the very first item in list when there are 10 measurements

        if mean(rollingList) <= voltLimit:  # <= voltLimit for Discharging # >= voltLimit for Charging
            # print('break')
            break                           # breaks out of while loop when the specified condition is met
    iteration += 1

    cell_Dict.update({'Capacity Time': measTimeL, 'Capacity Voltage': voltageL})

    time.sleep(10)      # 30 second between measurements

    # saves data every 2 minutes (120 seconds) = 12 iterations
    if (iteration % 12):
        tSave = threading.Thread(save_DF)
        tSave.start()

# turn relay to NC, thus DC Load Off
bk_POS.write(0)
bk_GND.write(0)


print("Testing Complete")
