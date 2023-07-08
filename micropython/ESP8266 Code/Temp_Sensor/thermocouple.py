# import machine
from machine import Pin, SPI
from time import sleep
import conf


def temp_c(data):
    """translate binary response into degreee C"""
    temp = data[0] << 8 | data[1]
    if temp & 0x0001:
        return float("NaN")  # Fault reading data.
    temp >>= 2
    if temp & 0x2000:
        temp -= 16384  # Sign bit set, take 2's compliment.
    return temp * 0.25


def callibrated_reading(temperature):
    """thermocouples may need callibrated
    coefficients should be stored in the config file
    2nd order can be used if non-linear
    set first coeficient to 0 for linear"""
    # TODO need to pass in callibration parameters defined in some config file
    # callibrate each thermocouple using 2nd order polynomial
    # for linear, set first coefficiet to 0
    coef2 = -0.01053
    coef1 = 1.90714
    offset = -15.35578
    temp_corrected = (
        (coef2 * temperature * temperature) + (coef1 * temperature) + offset
    )  # sensor #1 5/19/2023
    return temp_corrected

def initReadings(readings):
    for key in readings.keys():
        readings[key][2] = 0.0 # 3rd position is temp value
    return readings

def catReadings(readings):
    strReadings = ''
    for key in readings.keys():
        strReadings =+ readings[key][2] # 2nd position is temp value
    return strReading3rd

def read_thermocouple(cs_pin, spi):
    """reads one thermocouple from given CS pin and spi object"""
    raw_data = bytearray(4)

    S0 = Pin(16, Pin.OUT)
    S0.on()
    S1 = Pin(5, Pin.OUT)
    S1.on()
    S2 = Pin(4, Pin.OUT)
    S2.on()
    S3 = Pin(0, Pin.OUT)
    S3.on()
    S4 = Pin(2, Pin.OUT)
    S4.on() # signal low to read, default high

    # brute force testing
    if cs_pin == 1:
        S0.off()
        S1.on()
        S2.on()
        S3.on()
        S4.on()
    elif cs_pin == 2:
        S0.on()
        S1.off()
        S2.on()
        S3.on()
        S4.on()
    elif cs_pin == 3:
        S0.on()
        S1.on()
        S2.off()
        S3.on()
        S4.on()
    elif cs_pin == 4:
        S0.on()
        S1.on()
        S2.on()
        S3.off()
        S4.on()
    elif cs_pin == 5:
        S0.on()
        S1.on()
        S2.on()
        S3.on()
        S4.off()

    sleep(0.250) # 250 ms
    spi.readinto(raw_data)
    temp = temp_c(raw_data)

    return temp


def read_thermocouples(readings):
    """setup spi connection, read all thermocouples, close spi connection"""

    tspi = SPI(1, baudrate=5000000, polarity=0, phase=0)

    # print(readings)

    for key in readings.keys():
        cs_pin = readings[key][0] # first position is pin number
        readings[key][2] = read_thermocouple(cs_pin, tspi) # 3rd position is temp value
        print(f'{key}: temp: {readings[key][2]}')
        # sleep(1)

    # TODO need to place possible callibration call
    # callibration = []

    # TODO put in some error checking to ensure spi is released
    tspi.deinit()

    return readings
