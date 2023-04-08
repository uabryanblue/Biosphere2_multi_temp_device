# boot.py -- run on boot-up

from machine import Pin
import network

try:
  import usocket as socket
except:
  import socket

# import db_post

import esp
esp.osdebug(None)

import gc    
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

import ntptime
import time

#if needed, overwrite default time server
ntptime.host = "1.europe.pool.ntp.org"

try:
    print("Local time before synchronization：%s" %str(time.localtime()))
    #make sure to have internet connection
    ntptime.settime()
    print("Local time after synchronization：%s" %str(time.localtime()))
except:
    print("Error syncing time")


led = Pin(2, Pin.OUT)
# initialize the led as on
led.on()
