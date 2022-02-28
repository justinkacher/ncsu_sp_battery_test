import ctypes                     # import the C compatible data types
from sys import platform, path    # this is needed to check the OS type and get the PATH
from os import sep                # OS specific file path separators
from time import sleep, time



# load the dynamic library, get constants path (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
    constants_path = "C:" + sep + "Program Files (x86)" + sep + "Digilent" + sep + "WaveFormsSDK" + sep + "samples" + sep + "py"
elif platform.startswith("darwin"):
    # on macOS
    lib_path = sep + "Library" + sep + "Frameworks" + sep + "dwf.framework" + sep + "dwf"
    dwf = ctypes.cdll.LoadLibrary(lib_path)
    constants_path = sep + "Applications" + sep + "WaveForms.app" + sep + "Contents" + sep + "Resources" + sep + "SDK" + sep + "samples" + sep + "py"
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")
    constants_path = sep + "usr" + sep + "share" + sep + "digilent" + sep + "waveforms" + sep + "samples" + sep + "py"

# import constants
path.append(constants_path)
import dwfconstants as constants



class function:
    """ function names """
    custom = constants.funcCustom
    sine = constants.funcSine
    square = constants.funcSquare
    triangle = constants.funcTriangle
    noise = constants.funcNoise
    dc = constants.funcDC
    pulse = constants.funcPulse
    trapezium = constants.funcTrapezium
    sine_power = constants.funcSinePower
    ramp_up = constants.funcRampUp
    ramp_down = constants.funcRampDown




def open():
    '''
        open the first available device
    '''
    # this is the device handle - it will be used by all functions to "address" the connected device
    device_handle = ctypes.c_int()

    # connect to the first available device
    dwf.FDwfDeviceOpen(ctypes.c_int(-1), ctypes.byref(device_handle))
    return device_handle




#close connection
def close(device_handle):
    """
        close a specific device
    """
    dwf.FDwfDeviceClose(device_handle)
    return




##Generate a signal
def generate(device_handle, channel, function, offset, frequency=1e03, amplitude=2.2, symmetry=50, wait=0, run_time=0, repeat=0, data=[]):
    """
        generate an analog signal

        parameters: - device handle
                    - the selected wavegen channel (1-2)
                    - function - possible: custom, sine, square, triangle, noise, ds, pulse, trapezium, sine_power, ramp_up, ramp_down
                    - offset voltage in Volts
                    - frequency in Hz, default is 1KHz
                    - amplitude in Volts, default is 1V
                    - signal symmetry in percentage, default is 50%
                    - wait time in seconds, default is 0s
                    - run time in seconds, default is infinite (0)
                    - repeat count, default is infinite (0)
                    - data - list of voltages, used only if function=custom, default is empty
    """
    # enable channel
    channel = ctypes.c_int(channel - 1)
    dwf.FDwfAnalogOutNodeEnableSet(device_handle, channel, constants.AnalogOutNodeCarrier, ctypes.c_bool(True))
    
    # set function type
    dwf.FDwfAnalogOutNodeFunctionSet(device_handle, channel, constants.AnalogOutNodeCarrier, function)
    
    # load data if the function type is custom
    if function == constants.funcCustom:
        data_length = len(data)
        buffer = (ctypes.c_double * data_length)()
        for index in range(0, len(buffer)):
            buffer[index] = ctypes.c_double(data[index])
        dwf.FDwfAnalogOutNodeDataSet(device_handle, channel, constants.AnalogOutNodeCarrier, buffer, ctypes.c_int(data_length))
    
    # set frequency
    dwf.FDwfAnalogOutNodeFrequencySet(device_handle, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(frequency))
    
    # set amplitude or DC voltage
    dwf.FDwfAnalogOutNodeAmplitudeSet(device_handle, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(amplitude))
    
    # set offset
    dwf.FDwfAnalogOutNodeOffsetSet(device_handle, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(offset))
    
    # set symmetry
    dwf.FDwfAnalogOutNodeSymmetrySet(device_handle, channel, constants.AnalogOutNodeCarrier, ctypes.c_double(symmetry))
    
    # set running time limit
    dwf.FDwfAnalogOutRunSet(device_handle, channel, ctypes.c_double(run_time))
    
    # set wait time before start
    dwf.FDwfAnalogOutWaitSet(device_handle, channel, ctypes.c_double(wait))
    
    # set number of repeating cycles
    dwf.FDwfAnalogOutRepeatSet(device_handle, channel, ctypes.c_int(repeat))
    
    # start
    dwf.FDwfAnalogOutConfigure(device_handle, channel, ctypes.c_bool(True))
    return



#measure a voltage
def measure(device_handle, channel):
    """
        measure a voltage

        parameters: - device handler
                    - the selected oscilloscope channel (1-2, or 1-4)
        
        returns:    - the measured voltage in Volts
    """
    # set up the instrument
    dwf.FDwfAnalogInConfigure(device_handle, ctypes.c_bool(False), ctypes.c_bool(False))
    
    # read data to an internal buffer
    dwf.FDwfAnalogInStatus(device_handle, ctypes.c_bool(False), ctypes.c_int(0))
    
    # extract data from that buffer
    voltage = ctypes.c_double()   # variable to store the measured voltage
    dwf.FDwfAnalogInStatusSample(device_handle, ctypes.c_int(channel - 1), ctypes.byref(voltage))
    
    # store the result as float
    voltage = voltage.value
    return voltage

# def analog_impedance():
#     dwf.FDwfAnalogImpedanceReset(device_handle)
#     dwf.FDwfAnalogImpedanceModeSet(device_handle, ctypes.c_int(0))
#     dwf.FDwfAnalogImpedanceReferenceSet(device_handle, ctypes.c_double(1.2))
#     dwf.FDwfAnalogImpedanceReferenceGet(device_handle, ctypes.c_double(1.2))
# ## check page 97 of amazonaws.


input('press enter >>')


device_handle = open()              # open connection

generate(device_handle, 1, function.sine, 0)      #device_handle, channel, function, offset, frequency=1e03, amplitude=2.2, symmetry=50, wait=0, run_time=0, repeat=0, data=[]
time.sleep(2)


v1 = measure(device_handle, 1)      # measure pin 1
v2 = measure(device_handle, 2)      # measure pin 2
print("site 1 measure: ", v1, ", site 2 measure: ", v2)


close(device_handle)        # end connection