import pyvisa
import time
import pandas as pd
import numpy as np
from scipy.stats import linregress
from statistics import mean



# a Keithley 2450 SourceMeter is used for the open voltage reading, voltage reading during discharge,
# and both the source and meter for impedence testing

rm = pyvisa.ResourceManager()
#print(rm.list_resources())     # returns a tuple of connected devices # 'USB0::0x05E6::0x2450::04366211::INSTR'
keithley = rm.open_resource('USB0::0x05E6::0x2450::04366211::INSTR')
# print(keithley.query("*IDN?"))      # query's the Identity of the device connected
keithley.write('*RST')      # first line is to reset the instrument




# BK 8502 DC Load Supply is used for to discharge the cells at 10A
# a relay is used to turn on/off the load supply connection
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.board)
GPIO.setup(17, GPIO.OUT)





## Open Circuit Voltage
# battery connection:
# Sense Hi connect to positive terminal
# Sense Lo connect to negative terminal
# returns voltage measurement
def meas_VOC():
    keithley.write('*RST')                  # first line is to reset the instrument
    keithley.write('SENS:CURR:RSEN OFF')    # OFF = 2-Wire mode #  set On for 4-wire sense mode
    keithley.write('SENS:FUNC "VOLT"')      # set measure, sense, to voltage
    keithley.write('READ? "defbuffer1"')    # a ? is used for a query command otherwise is a set command
    voltage = keithley.read()               # defbuffer1 returns sense value
    return voltage


##  DC Internal Resistance (DC Impedance Test)
# battery connection Keithley:
# Sense Hi and Force Hi connect to positive terminal
# Sense Lo and Force Lo connect to negative terminal

# four sense probe. Keithley measure current in terms of ohm
def dc_Impedance():
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

    keithley.write('READ? "defbuffer1"')
    impedance = keithley.read()                         # units = Ohm
    # print(impedance)
    impedanceL.append(float(impedance))

    keithley.write('OUTP OFF')
    return impedance




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
def full_Capacity_BK8502():
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

    GPIO.output(17, 1)      # turn relay, thus DC Load, ON
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
        time.sleep(1)      # sleep is in seconds    # 1 second between measurements

    GPIO.output(17, 0)      # turn relay, thus DC Load, OFF

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

    keithley.write('*RST')      # first line is to reset the instrument
    keithley.write('OUTP:SMOD HIMP')                    # turn on high-impedance output mode
    keithley.write('SENS:CURR:RSEN ON')                 # set to 4-wire sense mode  # OFF = 2-Wire mode
    keithley.write('SENS:FUNC "CURR"')                  # set measure, sense, to current
    keithley.write(f'SENS:CURR:RANG {currentRange}')    # set current range # can also be 'SENS:CURR:RANG:AUTO ON'
    #keithley.write('SENS:CURR:UNIT OHM')               # set measure units to Ohm, can also be Watt or Amp
    keithley.write('SOUR:FUNC VOLT')                    # set source to voltage
    keithley.write(f'SOUR:VOLT {sourceVoltage}')        # set output voltage => discharge or charge test
    keithley.write('SOUR:VOLT:READ:BACK ON')            # turn on source read back
    keithley.write(f'SOUR:VOLT:RANG {voltageRange}')    # set source range
    keithley.write(f'SOUR:VOLT:ILIM {sourceLimit}')     # set source (current) limit
    keithley.write('OUTP ON')                           # turn on output, source

    iteration = 1           # iteration must start at 1 for Keithly write
    voltLimit = 2.75        # voltage which to stop the test
    currentL = []           # list of current readings; should be constant
    voltageL = []           # list of voltage readings
    measTimeL = []          # list of times the measurements occurred

    rollingList = []

    # 7. read load current, source voltage, and time stamp
    # 8. stop tset when battery reaches desired voltage

    while iteration >= 0:    # infinite while loop; breaks when voltLimit is reached
        keithley.write('READ? "defbuffer1"')        # a ? is used for a query command otherwise is a set command
        current = keithley.read()                   # a query command asks the instrument to return specifed information # a read is required before next set or query
        print(current)
        currentL.append(float(current))
        keithley.write(f'TRAC:DATA? {iteration}, {iteration},"defbuffer1", SOUR')       # reads source value
        volt = keithley.read()
        print(volt)
        voltageL.append(float(volt))
        keithley.write(f'TRAC:DATA? {iteration}, {iteration}, "defbuffer1", REL')
        timeSec = keithley.read()
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

    keithley.write('OUTP OFF')
    return currentL, voltageL , measTimeL



## Ratio Capacity Test
# Takes voltage discharge for 30 seconds
# Comapare to baseline of full capacity cells by impedence

# returns lists of currentL, voltageL , measTimeL
def ratio_Capacity_BK8502():
    keithley.write('*RST')                              # first line is to reset the instrument
    keithley.write('OUTP:SMOD HIMP')                    # turn on high-impedance output mode
#    keithley.write('SENS:CURR:RSEN OFF')                # set to 4-wire sense mode  # OFF = 2-Wire mode # by default?
    keithley.write('SENS:FUNC "VOLT"')                  # set measure, sense, to current
    keithley.write('SENS:CURR:RANG:AUTO ON')            # set current range to auto

    stopTime = 30           # discharge for 30 seconds
    testTime = 0            # initiate testTime to zero seconds
    voltageL = []           # list of voltage readings
    measTimeL = []          # list of times of readings

    GPIO.output(17, 1)      # turn relay, thus DC Load, ON
    startTime = time.time()

    while testTime >= stopTime:    # loop until 30 seconds, stoptime has passed
        keithley.write('READ? "defbuffer1"')        # get voltage sense reading
        voltage = keithley.read()
        # print(voltage)
        voltageL.append(float(voltage))

        time = time.time() - startTime
        measTimeL.append(float(time))

        time.sleep(1)      # sleep is in seconds    # 1 second between measurements

    GPIO.output(17, 0)      # turn relay, thus DC Load, OFF

    return currentL, voltageL, measTimeL


