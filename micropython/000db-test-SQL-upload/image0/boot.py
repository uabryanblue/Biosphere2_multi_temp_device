# Biosphere 2 remote sensing project
# Bryan Blue
# bryanblue@arizona.edu
# Spring 2023


try:
  import usocket as socket
except:
  import socket

# import db_post
# this is a config file to be used to pass values that can change dynamically
import conf
print("loaded config")
print(conf.PORT)

import esp
esp.osdebug(None)
import gc  
from machine import Pin
import network
import ntptime
import time

gc.collect()

# setup netword connection
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(conf.WAP_SSID, conf.WAP_PSWD)
while station.isconnected() == False:
  pass
print('Connection successful')
print(f'STATION: {station.ifconfig()}')

# set current date time with appropriate offset for timezone -7 is Tucson
ntptime.host = conf.NTP_HOST
time.localtime(time.time() + conf.UTC_OFFSET)
try:
    print("Local time before synchronization：%s" %str(time.localtime()))
    #make sure to have internet connection
    ntptime.settime()
    print("Local time after synchronization：%s" %str(time.localtime(time.time() + UTC_OFFSET)))
except:
    print("Error syncing time")

# initialize pin for led control
led = Pin(2, Pin.OUT)
# initialize the led as on
led.on()
