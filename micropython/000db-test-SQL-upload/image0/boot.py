"""
 Biosphere 2 remote sensing project
 Bryan Blue
  bryanblue@arizona.edu
 Spring 2023
"""

import gc
import time
import esp

esp.osdebug(None)
from machine import Pin
import network
import ntptime

# this is a config file to be used to pass values that can change dynamically
import conf

try:
    import usocket as socket
except:
    import socket

gc.collect()
# setup netword connection
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(conf.WAP_SSID, conf.WAP_PSWD)
while station.isconnected() is False:
    pass
print("Connection successful")
print(f"STATION: {station.ifconfig()}")

# set current date time with appropriate offset for timezone -7 is Tucson
ntptime.host = conf.NTP_HOST
time.localtime(time.time() + conf.UTC_OFFSET)
try:
    print(f"Local time befor NTP: {str(time.localtime() + conf.UTC_OFFSET)}")
    # print("Local time before synchronization：%s" % str(time.localtime()))
    # make sure to have internet connection
    ntptime.settime()
    print(f"Local time befor NTP: {str(time.localtime() + conf.UTC_OFFSET)}")
    # print(
    #     "Local time after synchronization：%s"
    #     % str(time.localtime(time.time() + conf.UTC_OFFSET))
    # )
except:
    print("Error syncing time")

# initialize pin for led control
led = Pin(2, Pin.OUT)
# initialize the led as on
led.on()
