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
def send(s,command):
    command += "\n"
    s.send(command.encode())
    return

def recieve(s):
    return s.recv(1024).decode()

def query(s,command):
    send(s,command)
    return recieve(s)


#initialize connection and reset
s = socket.socket()
s.connect(TCP_IP,TCP_Port)
send(s,"*RST")
print("ID: ",query(s,"*IDN?"))







# a Keithley 2450 SourceMeter is used for the open voltage reading, voltage reading during discharge,
# and both the source and meter for impedence testing

# rm = pyvisa.ResourceManager()
# #print(rm.list_resources())     # returns a tuple of connected devices # 'USB0::0x05E6::0x2450::04366211::INSTR'
# keithley = rm.open_resource('USB0::0x05E6::0x2450::04366211::INSTR')
# # print(keithley.query("*IDN?"))      # query's the Identity of the device connected
# send('*RST')      # first line is to reset the instrument




# BK 8502 DC Load Supply is used for to discharge the cells at 10A
# a relay is used to turn on/off the load supply connection
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.board)
GPIO.setup(17, GPIO.OUT)

# Relay 1: BK8502 Load ground - NC = nothing, NO = battery 1
# Relay 2: Keithley Sense ground - NC = battery 1, NO = battery 2
# Relay 3: Keithley Force ground - NC = battery 1, NO = battery 2
# Relay 4: BK8502 Load ground - NC = nothing, NO = battery 2
# Relay 5: BK8502 Load pos - NC = nothing, NO = battery 1
# Realy 6: Keithley Force pos - NC = battery 1, NO = battery 2
# Relay 7: Keithley Force pos - NC = battery 1, NO = battery 2
# Relay 8: BK8502 Load pos - NC = nothing, NO = battery 2
# Relay 9: LED ground - NC = nothing, NO = Battery 1 indicator
# Relay 10: LED ground - NC = nothing, NO = Battery 2 indicator

relays = {'R1': 17, 'R2': 17, 'R3': 17, 'R4': 17, 'R5': 17, 'R6': 17, 'R7': 17, 'R8': 17, 'LED_1': 17, 'LED_2': 17}

# loop to set up each relay pin to output 
for key, value in relays():
   GPIO.setup(value, GPIO.OUT)      # GPIO.setup(17, GPIO.OUT)


# turn ON LED for which battery is being tested
def start_test_LED(battery):
    if battery is 1:
        GPIO.output(relays['LED_1'], 1)      # LED 1 = R8 # relays on to NO positions
    if battery is 2:
        GPIO.output(relays['LED_2'], 1)      # LED 2 = R9 # relays on to NO positions

# turn OFF LED for which battery is being tested
def finish_test_LED(battery):
    if battery is 1:
        GPIO.output(relays['LED_1'],0)      # LED 1 = R8 # relays off to NC positions
    if battery is 2:
        GPIO.output(relays['LED_2'], 1)      # LED 2 = R9 # relays off to NC positions


## Open Circuit Voltage
# battery connection:
# Sense Hi connect to positive terminal
# Sense Lo connect to negative terminal
# returns voltage measurement
def meas_VOC(battery):
    # set keithley sense pos and sense gnd to battery holder 1 or 2 that is being tested
    if battery is 1:
        GPIO.output(relays['R7'], 0)      # sense pos = R7 # relays off to NC positions
        GPIO.output(relays['R2'], 0)      # sense gnd = R2 # relays off to NC positions
    if battery is 2:
        GPIO.output(relays['R7'], 1)      # sense pos = R7 # relays on to NO positions
        GPIO.output(relays['R2'], 1)      # sense gnd = R2 # relays on to NO positions

    send(s,"*RST")                  # first line is to reset the instrument
    send(s,'SENS:CURR:RSEN OFF')    # OFF = 2-Wire mode #  set On for 4-wire sense mode
    send(s,'SENS:FUNC "VOLT"')      # set measure, sense, to voltage

    # loop 10 times and compute the average Voc
    vocL = []
    for i in range(10):
        send(s,'READ? "defbuffer1"')    # a ? is used for a query command otherwise is a set command
        voltage = recieve(s)               # defbuffer1 returns sense value
        vocL.append(voltage)


    return mean(vocL)


##  DC Internal Resistance (DC Impedance Test)
# battery connection Keithley:
# Sense Hi and Force Hi connect to positive terminal
# Sense Lo and Force Lo connect to negative terminal

# four sense probe. Keithley measure current in terms of ohm
def dc_Impedance(battery):
    # set keithley sense pos and sense gnd to battery holder 1 or 2 that is being tested
    # set keithley force pos and force gnd to battery holder 1 or 2 that is being tested
    if battery is 1:
        GPIO.output(relays['R7'], 0)      # sense pos = R7 # relays off to NC positions
        GPIO.output(relays['R2'], 0)      # sense gnd = R2 # relays off to NC positions
        GPIO.output(relays['R6'], 0)      # force pos = R6 # relays off to NC positions
        GPIO.output(relays['R3'], 0)      # force gnd = R3 # relays off to NC positions
    if battery is 2:
        GPIO.output(relays['R7'], 1)      # sense pos = R7 # relays on to NO positions
        GPIO.output(relays['R2'], 1)      # sense gnd = R2 # relays on to NO positions
        GPIO.output(relays['R6'], 1)      # force pos = R6 # relays off to NO positions
        GPIO.output(relays['R3'], 1)      # force gnd = R3 # relays off to NO positions


    sourceVoltage = 2.65          # Charging: VSource > VBattery; Discharging: VS < VB # 18650 is 3.7v; max charging is 4.2v and min discharge final is 2.75
    voltageRange = 20            # 20mV, 200mV, 2V, 20V, 200V
    sourceLimit = 1.05              # Current Limit = Charge or Discharge rate # units A => 460e-3 A =.46 A = 460mA
    currentRange = 1             # Max 1.05A

    send('*RST')      # first line is to reset the instrument
    send('OUTP:SMOD HIMP')                    # turn on high-impedance output mode
    send('SENS:CURR:RSEN ON')                 # set to 4-wire sense mode  # OFF = 2-Wire mode
    send('SENS:FUNC "CURR"')                  # set measure, sense, to current
    send(f'SENS:CURR:RANG {currentRange}')    # set current range # can also be 'SENS:CURR:RANG:AUTO ON'
    send('SENS:CURR:UNIT OHM')               # set measure units to Ohm, can also be Watt or Amp
    send('SOUR:FUNC VOLT')                    # set source to voltage
    send(f'SOUR:VOLT {sourceVoltage}')        # set output voltage => discharge or charge test
    send('SOUR:VOLT:READ:BACK ON')            # turn on source read back
    send(f'SOUR:VOLT:RANG {voltageRange}')    # set source range
    send(f'SOUR:VOLT:ILIM {sourceLimit}')     # set source (current) limit
    send('OUTP ON')                           # turn on output, source

    time.sleep(5)   # to let the battery reach a steady state discharge

    # loop 10 times to and return the average DC impedance
    impedanceL = []
    for i in range(10):
        send('READ? "defbuffer1"')
        impedance = recieve()                         # units = Ohm
        # print(impedance)
        impedanceL.append(float(impedance))

    send('OUTP OFF')      # turn keithley
    return mean(impedanceL)




## linear sweep DC impedance
# Apply a current and measure voltage = resistance
# (V2-V1)/(I2-I1) = DC internal resistance
# current sweep: current limit is linearly changed and voltage response is observed, giving the resistance as the slope of the lined
# Kiethley: set voltage source to discharge or charge and ues current limit to set the constant current level
# returns slope = impedance value in along with list of voltage and currents used to calculate impedance
# currentLimit = np.linespace(0, 0.1, 25)     # returns array; start value, end value, number of points
# slope, intercept, r_value, p_value, std_err = linregress(x, y)

## AC Internal Resistance
# battery connection:
# Sense Hi and Force Hi connect to positive terminal
# Sense Lo and Force Lo connect to negative terminal





## Capacity Test
# BK8502 needs to be set to 10A discharge
# battery connection:
# Keithley Sense Hi and Lo connected to postive (red) and negative (black) wires respectfully
# BK8502 Load High connect to positive (red) terminal
# BK8502 Ground connect to normally open (NO) relay, relay Com connect to cell negative (black) wire

# Physical set up required
    # 1. Turn on BK8502: Press on Button in
    # 2. Turn on Supply: Press ## Button and make sure it says "10.0A" and "On" on the display
    # To set BK8502 load to 10A:

# returns list of currentL, voltageL , measTimeL
def full_Capacity_BK8502(battery):
    # set keithley sense pos and sense gnd to battery holder 1 or 2 that is being tested
    # set BK8502 load pos on for battery holder 1 or 2 that is being tested
    # set BK8502 load gnd on for batter holder 1 or 2 that is being tested
    if battery is 1:
        GPIO.output(relays['R7'], 0)      # sense pos = R7 # relays off to NC positions
        GPIO.output(relays['R2'], 0)      # sense gnd = R2 # relays off to NC positions
        GPIO.output(relays['R5'], 1)      # load pos = R5 # relays on to NO positions
        GPIO.output(relays['R3'], 1)      # load gnd = R3 # relays on to NO positions
    if battery is 2:
        GPIO.output(relays['R7'], 1)      # sense pos = R7 # relays on to NO positions
        GPIO.output(relays['R2'], 1)      # sense gnd = R2 # relays on to NO positions
        GPIO.output(relays['R8'], 1)      # load pos = R5 # relays on to NO positions
        GPIO.output(relays['R3'], 1)      # load gnd = R3 # relays on to NO positions




    send('*RST')                              # first line is to reset the instrument
    send('OUTP:SMOD HIMP')                    # turn on high-impedance output mode
    send('SENS:CURR:RSEN OFF')                # set to 4-wire sense mode  # OFF = 2-Wire mode # by default?
    send('SENS:FUNC "VOLT"')                  # set measure, sense, to current
    send('SENS:CURR:RANG:AUTO ON')            # set current range to auto

    iteration = 1           # iteration must start at 1 for Keithly write
    voltLimit = 2.75        # voltage which to stop the test
    voltageL = []           # list of voltage readings
    measTimeL = []          # list of times of readings

    rollingList = []        # list of voltage rolling  averaging for determinging when we reach the end test voltLimit; helps to ignore random drops/spikes

    GPIO.output(17, 1)      # turn relay, thus DC Load, ON
    startTime = time.time()

    while iteration >= 0:    # infinite while loop; breaks when voltLimit is reached
        #print(iteration)

        send('READ? "defbuffer1"')
        voltage = recieve()
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
        time.sleep(1)      # sleep is in seconds    # 1 second between measurements


    # turn relay, thus DC Load, OFF
    if battery is 1:
        GPIO.output(relays['R5'], 0)      # load pos = R5 # relays off to NC positions
        GPIO.output(relays['R3'], 0)      # load gnd = R3 # relays off to NC positions
    if battery is 2:
        GPIO.output(relays['R8'], 0)      # load pos = R5 # relays off to NC positions
        GPIO.output(relays['R3'], 0)      # load gnd = R3 # relays off to NC positions

    return currentL, voltageL, measTimeL


# keithley is limited to 1.05A max
# returns list of currentL, voltageL , measTimeL
def full_Capacity_Keithley():
    # full battery testing on keithley 2450 https://www.mouser.com/pdfdocs/RechargeableBattery_2450_AN1.PDF
    # 1. set to four-wire configuration
    # 2. set to source voltage, measure (sense) load current
    # 3. use high impedance output off state; opens output relay when output is turned off to prevent drainage when not testing
    # 4. set output voltage. Charging: VSource > VBattery (current is positive); Discharging: VS < VB (current is negative)
    # 5. turn voltage soucre readback function to measure battery voltage
    # 6. set current limit to charge or discharge the battery

    sourceVoltage = 2.65          # Charging: VSource > VBattery; Discharging: VS < VB # 18650 is 3.7v; max charging is 4.2v and min discharge final is 2.75
    voltageRange = 20            # 20mV, 200mV, 2V, 20V, 200V
    sourceLimit = 1.05              # Current Limit = Charge or Discharge rate # units A => 460e-3 A =.46 A = 460mA
    currentRange = 1             # Max 1.05A

    send('*RST')      # first line is to reset the instrument
    send('OUTP:SMOD HIMP')                    # turn on high-impedance output mode
    send('SENS:CURR:RSEN ON')                 # set to 4-wire sense mode  # OFF = 2-Wire mode
    send('SENS:FUNC "CURR"')                  # set measure, sense, to current
    send(f'SENS:CURR:RANG {currentRange}')    # set current range # can also be 'SENS:CURR:RANG:AUTO ON'
    #send('SENS:CURR:UNIT OHM')               # set measure units to Ohm, can also be Watt or Amp
    send('SOUR:FUNC VOLT')                    # set source to voltage
    send(f'SOUR:VOLT {sourceVoltage}')        # set output voltage => discharge or charge test
    send('SOUR:VOLT:READ:BACK ON')            # turn on source read back
    send(f'SOUR:VOLT:RANG {voltageRange}')    # set source range
    send(f'SOUR:VOLT:ILIM {sourceLimit}')     # set source (current) limit
    send('OUTP ON')                           # turn on output, source

    iteration = 1           # iteration must start at 1 for Keithly write
    voltLimit = 2.75        # voltage which to stop the test
    currentL = []           # list of current readings; should be constant
    voltageL = []           # list of voltage readings
    measTimeL = []          # list of times the measurements occurred

    rollingList = []

    # 7. read load current, source voltage, and time stamp
    # 8. stop tset when battery reaches desired voltage

    while iteration >= 0:    # infinite while loop; breaks when voltLimit is reached
        send('READ? "defbuffer1"')        # a ? is used for a query command otherwise is a set command
        current = recieve()                   # a query command asks the instrument to return specifed information # a read is required before next set or query
        print(current)
        currentL.append(float(current))
        send(f'TRAC:DATA? {iteration}, {iteration},"defbuffer1", SOUR')       # reads source value
        volt = recieve()
        print(volt)
        voltageL.append(float(volt))
        send(f'TRAC:DATA? {iteration}, {iteration}, "defbuffer1", REL')
        timeSec = recieve()
        print(float(timeSec))
        measTimeL.append(float(timeSec))

        # takes the rolling average voltage
        # this average is used to determine when to break from the tests
        # onlyy breaks after the first 15 measurements have been collected
        rollingList.append(float(volt))
        if len(rollingList) > 15:
            rollingList.pop(0)              #removes the very first item in list when there are 10 measurements

            if mean(rollingList) <= voltLimit:  # <= voltLimit for Discharging # >= voltLimit for Charging
                print('break')
                break                           # breaks out of while loop when the specified condition is met

        if iteration >= 15:
            break

        iteration += 1
        time.sleep(1)      # sleep is in seconds

    send('OUTP OFF')
    return currentL, voltageL , measTimeL



## Ratio Capacity Test
# Takes voltage discharge for 30 seconds
# Comapare to baseline of full capacity cells by impedence

# returns lists of currentL, voltageL , measTimeL
def ratio_Capacity_BK8502(battery):
    # set keithley sense pos and sense gnd to battery holder 1 or 2 that is being tested
    # set BK8502 load pos on for battery holder 1 or 2 that is being tested
    # set BK8502 load gnd on for batter holder 1 or 2 that is being tested
    if battery is 1:
        GPIO.output(relays['R7'], 0)      # sense pos = R7 # relays off to NC positions
        GPIO.output(relays['R2'], 0)      # sense gnd = R2 # relays off to NC positions
        GPIO.output(relays['R5'], 1)      # load pos = R5 # relays on to NO positions
        GPIO.output(relays['R3'], 1)      # load gnd = R3 # relays on to NO positions
    if battery is 2:
        GPIO.output(relays['R7'], 1)      # sense pos = R7 # relays on to NO positions
        GPIO.output(relays['R2'], 1)      # sense gnd = R2 # relays on to NO positions
        GPIO.output(relays['R8'], 1)      # load pos = R5 # relays on to NO positions
        GPIO.output(relays['R3'], 1)      # load gnd = R3 # relays on to NO positions

    send('*RST')                              # first line is to reset the instrument
    send('OUTP:SMOD HIMP')                    # turn on high-impedance output mode
#    send('SENS:CURR:RSEN OFF')                # set to 4-wire sense mode  # OFF = 2-Wire mode # by default?
    send('SENS:FUNC "VOLT"')                  # set measure, sense, to current
    send('SENS:CURR:RANG:AUTO ON')            # set current range to auto

    stopTime = 30           # discharge for 30 seconds
    testTime = 0            # initiate testTime to zero seconds
    voltageL = []           # list of voltage readings
    measTimeL = []          # list of times of readings

    GPIO.output(17, 1)      # turn relay, thus DC Load, ON
    startTime = time.time()

    while testTime >= stopTime:    # loop until 30 seconds, stoptime has passed
        send('READ? "defbuffer1"')        # get voltage sense reading
        voltage = recieve()
        # print(voltage)
        voltageL.append(float(voltage))

        time = time.time() - startTime
        measTimeL.append(float(time))

        time.sleep(1)      # sleep is in seconds    # 1 second between measurements

    GPIO.output(17, 0)      # turn relay, thus DC Load, OFF

    # turn relay, thus DC Load, OFF
    if battery is 1:
        GPIO.output(relays['R5'], 0)      # load pos = R5 # relays off to NC positions
        GPIO.output(relays['R3'], 0)      # load gnd = R3 # relays off to NC positions
    if battery is 2:
        GPIO.output(relays['R8'], 0)      # load pos = R5 # relays off to NC positions
        GPIO.output(relays['R3'], 0)      # load gnd = R3 # relays off to NC positions

    return currentL, voltageL, measTimeL
