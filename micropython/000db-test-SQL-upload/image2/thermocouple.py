# import machine
from machine import Pin, SPI
from time import sleep


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


# def read_thermocouple(cs_pin, spi):
#     """reads one thermocouple from given CS pin and spi object"""
#     raw_data = bytearray(4)
#     # cs = machine.Pin(cs_pin, machine.Pin.OUT)
#     # chip select needs to be low to take a reading, init high
#     # cs.on()

#     # read sensor and convert to degrees C
#     # cs.off()

#     S0 = Pin(16, Pin.OUT)
#     S0.off()
#     S1 = Pin(5, Pin.OUT)
#     S1.off()
#     S2 = Pin(4, Pin.OUT)
#     S2.off()
#     S3 = Pin(0, Pin.OUT)
#     S3.off()
#     cs = Pin(2, Pin.OUT)
#     cs.on() # signal low to read, default high
  
#     if cs_pin == 1:
#         S0.on()
#         S1.off()
#     else: #cs_pin == 1:
#         S0.off()
#         S1.on()

#     cs.off()
#     sleep(1)
#     print(f"CS:{cs.value()}  S0:{S0.value()}   S1:{S1.value()}")
#     spi.readinto(raw_data)
#     sleep(1)
#     cs.on()
#     temp = temp_c(raw_data)
#     print(f"temp:{temp}")
#     sleep(1)
#     return temp

def read_thermocouple(cs_pin, spi):
    """reads one thermocouple from given CS pin and spi object"""
    raw_data = bytearray(4)
    # cs = machine.Pin(cs_pin, machine.Pin.OUT)
    # chip select needs to be low to take a reading, init high
    # cs.on()

    # read sensor and convert to degrees C
    # cs.off()

    S0 = Pin(16, Pin.OUT)
    S0.off()
    S1 = Pin(5, Pin.OUT)
    S1.off()
    S2 = Pin(4, Pin.OUT)
    S2.off()
    S3 = Pin(0, Pin.OUT)
    S3.off()
    cs = Pin(2, Pin.OUT)
    cs.on() # signal low to read, default high
  
    if cs_pin == 1:
        S0.on()
        S1.off()
    else: #cs_pin == 1:
        S0.off()
        S1.on()

    cs.off()
    sleep(1)
    print(f"CS:{cs.value()}  S0:{S0.value()}   S1:{S1.value()}")
    spi.readinto(raw_data)
    sleep(1)
    cs.on()
    temp = temp_c(raw_data)
    print(f"temp:{temp}")
    sleep(1)
    return temp


def read_thermocouples(readings):
    """setup spi connection, read all thermocouples, close spi connection"""

    tspi = SPI(1, baudrate=5000000, polarity=0, phase=0)

    # print(readings)

    for key in readings.keys():
        cs_pin = key
        readings[key] = read_thermocouple(cs_pin, tspi)
        sleep(1)

    # TODO need to place possible callibration call
    # callibration = []

    # TODO put in some error checking to ensure spi is released
    tspi.deinit()

    return readings
