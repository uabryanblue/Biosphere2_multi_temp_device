"""
 Biosphere 2 remote sensing project
 Bryan Blue
  bryanblue@arizona.edu
 Spring 2023
"""
import conf
import gc
# import time
import realtc
import sd
import esp

esp.osdebug(None)

print("booting")
realtc.rtcinit()
print("set time")

sd.initSD()
###########################
# TURN ON LATER FOR ntp WiFi SUPPORT
# import network
# import ntptime

# # this is a config file to be used to pass values that can change dynamically
# import conf

# try:
#     import usocket as socket
# except:
#     import socket

# gc.collect()
# # setup netword connection
# station = network.WLAN(network.STA_IF)
# station.active(True)
# station.connect(conf.WAP_SSID, conf.WAP_PSWD)
# while station.isconnected() is False:
#     pass
# print("Connection successful")
# print(f"STATION: {station.ifconfig()}")

# # set current date time with appropriate offset for timezone -7 is Tucson
# ntptime.host = conf.NTP_HOST
# try:
#     print(f"Local time before NTP: {str(time.localtime())}")
#     ntptime.settime()
#     print(f"Local time after NTP: {str(time.localtime(time.time() + conf.UTC_OFFSET))}")
# except:
#     print("Error syncing time")

# initialize pin for led control
# led = Pin(2, Pin.OUT)
# # initialize the led as on
# led.on()





   