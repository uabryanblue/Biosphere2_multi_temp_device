import machine
from time import sleep


def temp_c(data):
    temp = data[0] << 8 | data[1]
    if temp & 0x0001:
        return float("NaN")  # Fault reading data.
    temp >>= 2
    if temp & 0x2000:
        temp -= 16384  # Sign bit set, take 2's compliment.
    return temp * 0.25


def takereading():
    data = bytearray(4)
    spi = machine.SPI(1, baudrate=5000000, polarity=0, phase=0)
    cs = machine.Pin(16, machine.Pin.OUT)  # main
    cs2 = machine.Pin(0, machine.Pin.OUT)  # try a second

    cs.on()
    cs2.on()

    # while True:

    cs.off()
    spi.readinto(data)
    cs.on()
    # print(f"TEMP1: {temp_c(data)}")
    temp1 = temp_c(data)

    # sleep(0.1)
    cs2.off()
    spi.readinto(data)

    # sleep(0.1)
    cs2.on()
    temp2 = temp_c(data)

    temp1_corrected = (
        (-0.01053 * temp1 * temp1) + 1.90714 * temp1 - 15.35578
    )  # sensor #1 5/19/2023

    # print(f"TEMP1: {temp1:5} TEMP1 Coorected: {temp1_corrected:5} TEMP2: {temp2:5}")

    return temp1, temp1_corrected, temp2

    # sleep(1)
