"""
Biosphere 2 remote sensing project
AUTHOR: Bryan Blue
EMAIL: bryanblue@arizona.edu
STARTED: 2023
"""

import gc
import time
import esp
import conf
from machine import Pin
import realtc
import sd
from time import sleep

esp.osdebug(None)


# pushes first real line of output
# to the line after the terminal garbage finishes
# "garbage" is due to mismatch in terminal speed on boot, not a bug
print("booting")

# set the on board RTC to the time from the DS3231
realtc.rtcinit()
print("set time")

# attach SD card module and mount the SD card, if one is present
sd.initSD(conf.LOG_MOUNT)
sleep(0.5)