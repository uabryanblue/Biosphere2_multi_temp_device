# Biosphere 2 remote sensing project
# Bryan Blue
# bryanblue@arizona.edu
# Spring 2023


try:
  import usocket as socket
except:
  import socket

# import db_post

import esp
esp.osdebug(None)
import gc  
from machine import Pin
import network
import ntptime
import time

gc.collect()

# setup netword connection
ssid = 'DEA_VAN3'
password = 'Help1Sago8!MoMo'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
  pass
print('Connection successful')
print(station.ifconfig())

#if needed, overwrite default time server
# ntptime.host = "1.europe.pool.ntp.org"
ntptime.host = "3.netbsd.pool.ntp.org"
UTC_OFFSET = -7 * 60 * 60 # arizona time
time.localtime(time.time() + UTC_OFFSET)

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
