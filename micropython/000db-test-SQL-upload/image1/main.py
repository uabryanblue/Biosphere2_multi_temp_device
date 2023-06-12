import machine
import time

import logger
import conf
import realtc
import sd
# import thermocouple
import lcd

import espnowex

print("START")
# status pin for logger, GPIO16/D0
D0 = machine.Pin(16, machine.Pin.OUT)
D0.on()

rtc = machine.RTC()

sta, ap = espnowex.wifi_reset()
esp_con = espnowex.init_esp_connection(sta)

# convert hex into readable mac address
RAW_MAC = espnowex.get_mac(sta)
MY_MAC = ':'.join(['{:02x}'.format(b) for b in RAW_MAC])
# print(f"My MAC:: {MY_MAC}")
print(f"My MAC addres:: {MY_MAC} raw MAC:: {RAW_MAC}")

logname = '/' + conf.LOG_MOUNT + "/" + conf.LOG_FILENAME

while True:
    print("going to listen for a message")
    host, msg = espnowex.esp_rx(esp_con)
    str_host = ':'.join(['{:02x}'.format(b) for b in host])
    # assumption data is utf-8, if not, it may fail
    str_msg = msg.decode('utf-8')
    D0.off() # turn LED on as a visual aid

    if msg == b'get_time':
        print(f"{host}, {str_host} requested the time")
        time.sleep(0.1) # let other side get ready
        # receiver blocked until time is received
        espnowex.esp_tx(esp_con, str(rtc.datetime()))
        D0.on()
        print("time sent")
    else:
        # str_host = host.decode('utf-8')
        logger.write_log(logname, str_host + ',' + str_msg)
    D0.on() # turn LED off as a visual aid
    


    # time.sleep(3)

print("dump log contents")
logger.cat_log(logname)





# ########### !!! if you don't close it, it will get overwritten
# when the next PYMAKR update is performed!!!!!!!!!!!
sd.closeSD('/' + conf.LOG_MOUNT)

