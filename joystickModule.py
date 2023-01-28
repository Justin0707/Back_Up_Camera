JOYSTICK_X = "/sys/bus/iio/devices/iio:device0/in_voltage2_raw"
JOYSTICK_Y = "/sys/bus/iio/devices/iio:device0/in_voltage3_raw"

A2D_MAX_READING = 4095
POSITIVE_DEADZONE = 0.5
NEGATIVE_DEADZONE = -0.5
INTERPOLATION_MAX_VALUE = 12

def readJoystickX():
    a2dReading = readFromFile(JOYSTICK_X)
    return convertReading(a2dReading)

def joystickYInterpolated():
    a2dReading = float(readFromFile(JOYSTICK_X))
    a2dReading = (a2dReading)/(A2D_MAX_READING)
    return round(a2dReading * INTERPOLATION_MAX_VALUE)

def readJoystickY():
    a2dReading = readFromFile(JOYSTICK_Y)
    return convertReading(a2dReading)

def readFromFile(fileName):
    file = open(fileName, "r")
    returnVal = file.readline()
    file.close()
    return (returnVal)

def convertReading(a2dReading):
    a2dReading = (a2dReading - (A2D_MAX_READING/2))/(A2D_MAX_READING/2)
    if a2dReading > POSITIVE_DEADZONE:
        return 1
    elif a2dReading < NEGATIVE_DEADZONE:
        return -1
    else:
        return 0