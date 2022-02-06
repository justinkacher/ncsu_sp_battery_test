#TRUE = active test
#FALSE = test is ended/inactive

from pickle import FALSE, TRUE
import config as config
import site1test
import site2test





def checkstate1():
    if config.site1state == TRUE:
        config.msgsite1 = "ERROR: Site 1 is Active"
    else:
        if config.IDscale == "--":
            config.msgsite1 = "No ID associated"
        else:
            site1test.runtest()
            config.msgsite1 = "Test Site Active\nDO NOT REMOVE"

def checkstate2():
    if config.site2state == TRUE:
        config.msgsite2 = "ERROR: Site 1 is Active"
    else:
        if config.IDscale == "--":
            config.msgsite2 = "No ID associated"
        else:
            site2test.runtest()
            config.msgsite2 = "Test Site Active\nDO NOT REMOVE"

def rmvcheckstate1():
    if config.site1state == TRUE:
        config.msgsite1 = "ERROR: Site 1 is Active"
    else:
        config.msgsite1 = "Remove"
        config.IDsite1 = "--"


def rmvcheckstate2():
    if config.site2state == TRUE:
        config.msgsite2 = "ERROR: Site 2 is Active"
    else:
        config.msgsite2 = "Remove"
        config.IDsite2 = "--"

