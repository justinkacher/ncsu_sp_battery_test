#import Battery_Test_Methods as BTM


from pickle import FALSE, TRUE
import config
import time


def runtest():
    #print('run test')
    config.IDsite1 = config.IDscale
    config.IDscale = "--"
    config.scalevalue = "--"
    config.site1state = TRUE
    #
    # BTM.meas_VOC()

