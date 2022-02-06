import config

print("test scale")
def tare():
    print("tareing")
    config.scalevalue = "--"



def read():
    config.IDscale = input("scale id")
    #to be replaced with scan

    print("reading")
    config.scalevalue = 420
    #save value associated with ID at this step
    #add confirmation print