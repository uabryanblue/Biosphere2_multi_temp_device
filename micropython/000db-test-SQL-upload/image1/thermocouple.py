import machine
from time import sleep


def temp_c(data):
    """ translate binary response into degreee C """
    temp = data[0] << 8 | data[1]
    if temp & 0x0001:
        return float("NaN")  # Fault reading data.
    temp >>= 2
    if temp & 0x2000:
        temp -= 16384  # Sign bit set, take 2's compliment.
    return temp * 0.25


def takereading():
    """
    take readings of all configured thermocouples
    use callibration equation to adjust to more precise readings
    TODO: this should be turned into a digital mux
    """

    data = bytearray(4)
    spi = machine.SPI(1, baudrate=5000000, polarity=0, phase=0)
    # need one pin for each chip select
    cs = machine.Pin(16, machine.Pin.OUT)
    cs2 = machine.Pin(0, machine.Pin.OUT) 

    # chip select needs to be low to take a reading, init high 
    cs.on()
    cs2.on()

    # read sensor and convert to degrees C
    cs.off()
    spi.readinto(data)
    cs.on()
    temp1 = temp_c(data)

    # read sensor and convert to degrees C
    cs2.off()
    spi.readinto(data)
    cs2.on()
    temp2 = temp_c(data)

    # callibrate each thermocouple and use corrected value
    temp1_corrected = (
        (-0.01053 * temp1 * temp1) + 1.90714 * temp1 - 15.35578
    )  # sensor #1 5/19/2023

    # TODO put in some error checking to ensure spi is released
    spi.deinit()

    return temp1, temp1_corrected, temp2
