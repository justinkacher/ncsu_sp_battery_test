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
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 2000  # Set Duration To 1000 ms == 1 second

# test change

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
keithley.write('OUTP:SMOD HIMP')  # turn on high-impedance output mode; so battery wont drain while just sitting




# Connect to Arduino
# sets serial connection with arduino uno and establish pin connections
arduinoPort = 'COM4'
arduinoB = pyfirmata.Arduino(arduinoPort)  # arduino uno #if MEGA then use ArduinoMega(arduinoPort)
it = pyfirmata.util.Iterator(arduinoB)
it.start()
# a: analog,  d: digital
# i: input, o: output, s: servo, p: pwm
# servo 0-180
# pwm 0-255 or a float value 0 to 1.0
bk_GND = arduinoB.get_pin('d:2:o')  # for relay
bk_POS = arduinoB.get_pin('d:3:o')  # for relay
# ensures both relays are off; set to NC position
bk_GND.write(1)
bk_POS.write(1)

cell_Dict = {}


# function to save the dataframe
# function to be called after test 1 and 2, and every 5 minutes during capasicty discharge test 3
def save_DF():
    # turn dictionary to dataframe
    # uses series so columns can be of differnt length

    df_battery_dict = pd.DataFrame({key: pd.Series(value) for key, value in cell_Dict.items()})
    df_battery_dict.to_excel(fileFolder + 'Test cell ' + cell_Dict['Cell Number'] + '.xlsx')

def set_forVoltageReading():
    keithley.write('SOUR:VOLT:RANG 20')

def voltage_Reading():

    keithley.write('OUTP ON')
    time.sleep(.5)

    keithley.write('MEAS:VOLT? "defbuffer1", READ')
    voltReading = keithley.read()

    keithley.write('OUTP OFF')

    # voltR = float(voltReading)
    # print(voltR)


    return float(voltReading)

# function takes current source limit
def SMU(sourceLimit):
    keithley.write(f'SOUR:VOLT:ILIM {sourceLimit}')  # set voltage source (current) limit

    keithley.write('READ? "defbuffer1"')
    current = (float(keithley.read()))

    keithley.write('READ? "defbuffer1", SOUR')  # a ? is used for a query command otherwise is a set command
    volt = float(keithley.read())  # defbuffer1 returns sense value

    return current, volt

print('Ensure proper connection and equipment is turned on')
cell_Name = input('>> Cell number: ')
cell_Dict = {'Cell Number': cell_Name}

input('Press Enter to start testing >> ')

# Test 1
print('   Starting Test 1/3: Measuring Voc...')

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




# keithley.write('SENS:FUNC "VOLT"')          # set measurement to voltage
# keithley.write(':SENS:VOLT:RSEN OFF')       # set to Two-Wire mode; the measurement is on Force HI/LOW
# keithley.write('SOUR:VOLT:RANG 20')
# keithley.write('SOUR:VOLT:READ:BACK ON')


# keithley.write('OUTP ON')
# time.sleep(1)
# keithley.write('READ? "defbuffer1", SOUR')
# voltR = keithley.read()
# keithley.write('OUTP OFF')
#
# print(voltR)
#
# sourceVoltage = 2.65  # Charging: VSource > VBattery; Discharging: VS < VB # 18650 is 3.7v; max charging is 4.2v and min discharge final is 2.75
# voltageRange = 20  # 20mV, 200mV, 2V, 20V, 200V
# sourceLimit = 0.2  # Current Limit = Charge or Discharge rate # units A => 460e-3 A =.46 A = 460mA
# currentRange = 1.05  # Max 1.05A
#
# keithley.write('*RST')  # first line is to reset the instrument
# keithley.write('OUTP:SMOD HIMP')  # turn on high-impedance output mode
# keithley.write('SENS:CURR:RSEN ON')  # set to 4-wire sense mode  # OFF = 2-Wire mode
# keithley.write('SENS:FUNC "CURR"')  # set measure, sense, to current
# keithley.write(f'SENS:CURR:RANG {currentRange}')  # set current range # can also be 'SENS:CURR:RANG:AUTO ON'
# keithley.write('SENS:CURR:UNIT AMP')  # set measure units to Ohm, can also be Watt or Amp
# keithley.write('SOUR:FUNC VOLT')  # set source to voltage
# keithley.write(f'SOUR:VOLT {sourceVoltage}')  # set output voltage => discharge or charge test
# keithley.write('SOUR:VOLT:READ:BACK ON')  # turn on source read back
# keithley.write(f'SOUR:VOLT:RANG {voltageRange}')  # set source range
# keithley.write(f'SOUR:VOLT:ILIM {sourceLimit}')  # set source (current) limit
# keithley.write('OUTP ON')  # turn on output, source
#
# # loop 10 times and compute the average Voc at a discharge of 0.1A
# vocL = []
# for i in range(10):
#     keithley.write('READ? "defbuffer1", SOUR')  # a ? is used for a query command otherwise is a set command
#     voltage_i = float(keithley.read())  # defbuffer1 returns sense value
#     vocL.append(voltage_i)
#
#     time.sleep(0.1)
#
# keithley.write('OUTP OFF')  # turn off keithley
#
# Voc = mean(vocL)
# cell_Dict['Voc (V)'] = Voc
# print("      Voc is {:.2f}".format(Voc))

# # Test 2
# print("   Starting Test 2/3: Measuring DC Impedance...")
# sourceVoltage = 2.65  # Charging: VSource > VBattery; Discharging: VS < VB # 18650 is 3.7v; max charging is 4.2v and min discharge final is 2.75
# voltageRange = 20  # 20mV, 200mV, 2V, 20V, 200V
# sourceLimit = np.linspace(0.1, 1, 10)     # returns array; start value, end value, number of points
#
# currentRange = 1.05  # Max 1.05A
#
# keithley.write('*RST')  # first line is to reset the instrument
# keithley.write('OUTP:SMOD HIMP')  # turn on high-impedance output mode
# keithley.write('SENS:CURR:RSEN ON')  # set to 4-wire sense mode  # OFF = 2-Wire mode
# keithley.write('SENS:FUNC "CURR"')  # set measure, sense, to current
# keithley.write(f'SENS:CURR:RANG {currentRange}')  # set current range # can also be 'SENS:CURR:RANG:AUTO ON'
# keithley.write('SENS:CURR:UNIT AMP')  # set measure units to Ohm, can also be Watt or Amp
# keithley.write('SOUR:FUNC VOLT')  # set source to voltage
# keithley.write(f'SOUR:VOLT {sourceVoltage}')  # set output voltage => discharge or charge test
# keithley.write('SOUR:VOLT:READ:BACK ON')  # turn on source read back
# keithley.write(f'SOUR:VOLT:RANG {voltageRange}')  # set source range
# keithley.write(f'SOUR:VOLT:ILIM {sourceLimit[0]}')  # set source (current) limit
# keithley.write('OUTP ON')  # turn on output, source
#
# # loop 10 times to and return the average DC impedance
# currentL_impedance = []
# voltL_impedance = []
# for i in range(len(sourceLimit)):
#     keithley.write(f'SOUR:VOLT:ILIM {sourceLimit[i]}')  # set source (current) limit
#     time.sleep(0.1)
#
#     keithley.write('READ? "defbuffer1"')
#     curr = keithley.read()  # units = Ohm
#     currentL_impedance.append(float(curr))
#
#     keithley.write('READ? "defbuffer1", SOUR')  # a ? is used for a query command otherwise is a set command
#     volt = float(keithley.read())  # defbuffer1 returns sense value
#     voltL_impedance.append(volt)
#
# keithley.write('OUTP OFF')  # turn off keithley
#
# impedanceL = []
# for i in range(len(voltL_impedance)-1):
#     DC_impedance = (voltL_impedance[i] - voltL_impedance[i+1]) / (currentL_impedance[i] - currentL_impedance[i+1])
#     # print(DC_impedance)
#     impedanceL.append(DC_impedance)
#
# impedance_Avg = mean(impedanceL)
# # print('current')
# # print(currentL_impedance)
# # print(' volt')
# # print(voltL_impedance)
#
# impedance = impedance_Avg*1000   # to get to milli- Ohms
#
# cell_Dict['DC Impedance (Ohms)'] = impedance
# print('      Impedance is {:.1f} m-Ohm'.format(impedance))

# Test 3
print("   Starting Test 2/3: Measuring DC Impedance...")
sourceVoltage = 2.65  # Charging: VSource > VBattery; Discharging: VS < VB # 18650 is 3.7v; max charging is 4.2v and min discharge final is 2.75
voltageRange = 20  # 20mV, 200mV, 2V, 20V, 200V
currentRange = 1.05  # Max 1.05A

keithley.write('*RST')  # first line is to reset the instrument
keithley.write('OUTP:SMOD HIMP')  # turn on high-impedance output mode
keithley.write('SENS:CURR:RSEN ON')  # set to 4-wire sense mode  # OFF = 2-Wire mode
keithley.write('SENS:FUNC "CURR"')  # set measure, sense, to current
keithley.write(f'SENS:CURR:RANG: AUTO')  # set current range # can also be 'SENS:CURR:RANG:AUTO ON'
keithley.write('SENS:CURR:UNIT AMP')  # set measure units to Ohm, can also be Watt or Amp
keithley.write('SOUR:FUNC VOLT')  # set source to voltage
keithley.write(f'SOUR:VOLT {sourceVoltage}')  # set output voltage => discharge or charge test
keithley.write('SOUR:VOLT:READ:BACK ON')  # turn on source read back
keithley.write(f'SOUR:VOLT:RANG {voltageRange}')  # set source range

keithley.write(f'SOUR:VOLT:ILIM {0.01}')  # set source (current) limit


# loop 10 times to and return the average DC impedance
currentL_impedance = []
voltL_impedance = []


hz = 1000       # run test at 1 kHz
freq_Time = 1/hz

neg_sampleRate = np.linspace(3.14159, 3.14159*2, 10)
neg_current_amplitude = np.sin(neg_sampleRate)*.5

pos_sampleRate = np.linspace(0, 6.28318, 10)      # just the upper, positive half of the sine wave
pos_current_amplitude = np.sin(pos_sampleRate)*.5


import matplotlib.pyplot as plt

plt.plot(pos_sampleRate, pos_current_amplitude)
plt.plot(neg_sampleRate, neg_current_amplitude)
plt.show()


keithley.write('OUTP ON')  # turn on output, source
startTime = time.time()
#loop ac twice = 2 seconds
for i in range(2):
    # set voltage to discharge; 2.6 V
    keithley.write(f'SOUR:VOLT {2.6}')
    # loop through , neg values first
    for i in neg_current_amplitude:
        current, voltage = SMU(i)
        currentL_impedance.append(current)
        voltL_impedance.append(voltage)


    # set voltage to charge; 4.2 V
    keithley.write(f'SOUR:VOLT {4.5}')
    # loop through charge, pos, values second
    for i in pos_current_amplitude:
        current, voltage = SMU(i)
        currentL_impedance.append(current)
        voltL_impedance.append(voltage)




keithley.write('OUTP OFF')  # turn off keithley

print(time.time()-startTime)
print(currentL_impedance)
print(voltL_impedance)



impedanceL = []
for i in range(len(voltL_impedance)-1):
    volt_sub = voltL_impedance[i] - voltL_impedance[i+1]
    curr_sub = currentL_impedance[i] - currentL_impedance[i+1]

    if volt_sub <= 0:
        volt_sub = .0001

    if curr_sub <= 0:
        curr_sub = .0001

    AC_impedance = volt_sub / curr_sub

    # AC_impedance = (voltL_impedance[i] - voltL_impedance[i + 1]) / (currentL_impedance[i] - currentL_impedance[i + 1])

    impedanceL.append(AC_impedance)

impedance_Avg = mean(impedanceL)
# print('current')
# print(currentL_impedance)
# print(' volt')
# print(voltL_impedance)

impedance = impedance_Avg*1000   # to get to milli- Ohms

cell_Dict['AC Impedance (Ohms)'] = impedance
print('      Impedance is {:.1f} m-Ohm'.format(impedance))











# # Test 4
# print("Disconnect Keithley Force wires and connect BK 8502 DC Load & then turn on")
# input("Press Enter to start test 3 >>")
# print("   Starting Test 4/4: Measuring Total Discharge...")
#
# keithley.write('*RST')  # first line is to reset the instrument # 2-Wire mode by default
# set_forVoltageReading()
#
# iteration = 1  # iteration must start at 1 for Keithly write
# voltLimit = 3.3  # voltage which to stop the test
# voltageL = []  # list of voltage readings
# measTimeL = []  # list of times of readings
#
# rollingList = []  # list of voltage rolling  averaging for determinging when we reach the end test voltLimit; helps to ignore random drops/spikes
#
# # turn relay to NO, thus DC Load ON
# bk_POS.write(0)
# bk_GND.write(0)
#
# startTime = time.time()
#
# while iteration >= 0:  # infinite while loop; breaks when voltLimit is reached
#     # print(iteration)
#
#     voltage = voltage_Reading()
#     print(voltage)
#     voltageL.append(float(voltage))
#
#     time_measure = time.time() - startTime
#     measTimeL.append(float(time_measure))
#
#     # takes the rolling average voltage
#     # this average is used to determine when to break from the tests
#     rollingList.append(float(voltage))
#     if len(rollingList) > 15:
#         rollingList.pop(0)  # removes the very first item in list when there are 10 measurements
#
#         if mean(rollingList) <= voltLimit:  # <= voltLimit for Discharging # >= voltLimit for Charging
#             # print('break')
#             break  # breaks out of while loop when the specified condition is met
#     iteration += 1
#
#
#     time.sleep(1)
#
#
#     cell_Dict.update({'Capacity Time': measTimeL, 'Capacity Voltage': voltageL})
#
#     # saves data every 150 seconds => 15 iterations
#     if iteration % 15:
#         tSave = threading.Thread(target=save_DF)
#         tSave.start()
#
#
#
#
# # turn relay to NC, thus DC Load Off
# bk_POS.write(1)
# bk_GND.write(1)
save_DF()
print("TURN OFF BK 8502")
print("Testing Complete")
winsound.Beep(frequency, duration)
