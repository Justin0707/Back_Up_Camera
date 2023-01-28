PHOTO_RESISTOR_VALUE = "/sys/bus/iio/devices/iio:device0/in_voltage1_raw"

MAX_READING = 4095
MAX_VALUE = 10

# Returns a value between 0 and 10
def PhotoResistor_getVoltage():
    reading = int(readFromFile(PHOTO_RESISTOR_VALUE))
    voltage = reading / MAX_READING
    voltage = round(voltage * MAX_VALUE)
    return voltage

def readFromFile(fileName):
    file = open(fileName, "r")
    returnVal = file.readline()
    file.close()
    return (returnVal)