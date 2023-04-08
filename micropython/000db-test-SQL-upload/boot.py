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

led = Pin(2, Pin.OUT)
# initialize the led as on
led.on()
