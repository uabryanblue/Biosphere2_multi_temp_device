# RTC module default I2C address is 0x57 (dec 87)
# address range is 0x50 to 0x57 using solder jumpers
# https://lastminuteengineers.com/ds3231-rtc-arduino-tutorial/

# HiLetgo DS3231 + AT24C32N 


# import from machiine I2C
# i2c = I2C(sda=machine.Pin(4), scl=machine.Pin(5))
# 

from machine import I2C, Pin, RTC
from ds3231_gen import *

def rtcinit():
    """get the time from the RTC DS3231 board and set the local RTC"""

    i2c = I2C(sda=machine.Pin(4), scl=machine.Pin(5))
    d = DS3231(i2c)
    rtc = RTC()
    print(f"DS3231 time: {d.get_time()}")
    print(f"local time: {time.localtime()}")
    YY, MM, DD, hh, mm, ss, wday, _ = d.get_time()
    rtc.datetime((YY, MM, DD, wday, hh, mm, ss, 0))

