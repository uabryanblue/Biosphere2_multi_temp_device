# RTC module default I2C address is 0x57 (dec 87)
# address range is 0x50 to 0x57 using solder jumpers
# https://lastminuteengineers.com/ds3231-rtc-arduino-tutorial/

# HiLetgo DS3231 + AT24C32N 
 
# to set the time on the DS3231 use a tuple as shown here
# d = DS3231(i2c)
# d.set_time((YY, MM, DD, hh, mm, ss, 0, 0))
# set time to 2023, May, 29, 7 am, 11 minutes, 1 second, NA, NA
# d.set_time((2023, 05, 29, 7, 11, 1, 0, 0))

from machine import I2C, Pin, RTC
from ds3231_gen import *

def rtcinit():
    """get the time from the RTC DS3231 board and set the local RTC"""
    rtc = RTC()
    i2c = I2C(sda=machine.Pin(4), scl=machine.Pin(5))
    d = DS3231(i2c)
    YY, MM, DD, hh, mm, ss, wday, _ = d.get_time()
    rtc.datetime((YY, MM, DD, wday, hh, mm, ss, 0))
    print(f"DS3231 time: {d.get_time()}")
    print(f"local time: {time.localtime()}")

