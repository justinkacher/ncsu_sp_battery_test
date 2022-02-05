#TRUE = active test
#FALSE = test is ended/inactive

from pickle import FALSE, TRUE
from time import sleep
import config as config

def starttest():
    if config.site1state==TRUE:
        config.msgsite1 = "ERROR: Site 1 is Active"
    else:
        config.msgsite1 = "Test Active\nDO NOT REMOVE"
        #turn on safety light
        #run tests

    
    if config.site2state == TRUE:
        config.msgsite2 = "ERROR: Site 2 is Active"
    else:
        config.msgsite2 = "Test Active\nDO NOT REMOVE"
        #turn on safety light
        # run tests




