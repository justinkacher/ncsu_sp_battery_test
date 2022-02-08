import Battery_Test_Methods as BTM

from pickle import FALSE, TRUE
import pandas as pd
import config
import time


def runtest():
    config.IDsite1 = config.IDscale
    config.IDscale = "--"
    config.scalevalue = "--"
    config.site1state = TRUE

    batterySite = 1

    battery_dict = {'Cell ID': config.site1state, 'Battery Test Holder': batterySite}

    # turn ON test site led
    BTM.start_test_LED(batterySite)

    # get the mean Voc
    voc = BTM.meas_VOC(batterySite)
    battery_dict['Voc'] = voc

    # get the mean DC Impedance
    impedance = BTM.dc_Impedance(batterySite)
    battery_dict['Impedance'] = impedance

    # perform ratio capacity testing
    # voltage is what we are interested in. Current should be constant
    currentL, voltageL, measTimeL = BTM.ratio_Capacity_BK8502(batterySite)
    battery_dict.update({'Capacity measurment times': measTimeL, 'Capacity voltage measurments': voltageL, 'Capacity current': currentL})

    # turn OFF test side led
    Battery_Test_Methods.finish_test_LED(batterySite)

    # turn dictionary to dataframe
    # uses series so columns can be of differnt length
    fileFolder = 'C:/Users/nwoodwa/Desktop/SolarPack/'
    df_battery_dict = pd.DataFrame({key: pd.Series(value) for key, value in battery_dict.items()})
    df_battery_dict.to_excel(fileFolder+'Test cell ' + str(config.site1state) + '.xlsx')
