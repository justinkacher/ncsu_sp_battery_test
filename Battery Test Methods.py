import pyvisa
import time
import pandas as pd
from statistics import mean

rm = pyvisa.ResourceManager()

#print(rm.list_resources())     # returns a tuple of connected devices # 'USB0::0x05E6::0x2450::04366211::INSTR'

keithley = rm.open_resource('USB0::0x05E6::0x2450::04366211::INSTR')

print(keithley.query("*IDN?"))      # query's the Identity of the device connected

