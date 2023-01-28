RED_SWITCH_VALUE = "/sys/class/gpio/gpio65/value"
GREEN_SWITCH_VALUE = "/sys/class/gpio/gpio46/value"
GREY_SWITCH_VALUE = "/sys/class/gpio/gpio47/value"

def Tactile_isGreenPressed():
    return float(readFromFile(GREEN_SWITCH_VALUE))

def Tactile_isRedPressed():
    return float(readFromFile(RED_SWITCH_VALUE))

def Tactile_isGreyPressed():
    return float(readFromFile(GREY_SWITCH_VALUE))

def readFromFile(fileName):
    file = open(fileName, "r")
    returnVal = file.readline()
    file.close()
    return (returnVal)