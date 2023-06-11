import machine
from time import sleep

import logger
import conf
import realtc
import sd
# import thermocouple
import lcd

import espnowex

print("START")

sta, ap = espnowex.wifi_reset()
esp_con = espnowex.init_esp_connection(sta)

# convert hex into readable mac address
RAW_MAC = espnowex.get_mac(sta)
MY_MAC = ':'.join(['{:02x}'.format(b) for b in RAW_MAC])
# print(f"My MAC:: {MY_MAC}")
print(f"My MAC addres:: {MY_MAC} raw MAC:: {RAW_MAC}")

logname = '/' + conf.LOG_MOUNT + "/" + conf.LOG_FILENAME

for i in range(3):
    print("going to listen for a response")
    host, msg = espnowex.esp_rx(esp_con)
    if msg == b'get_time':
        print(f"{host} requested the time")
    else:
        # assumption data is utf-8, if not, it may fail
        str_host = host.decode('utf-8')
        str_msg = msg.decode('utf-8')
        logger.write_log(logname, str_host + str_msg)
    


    sleep(3)

print("dump log contents")
logger.cat_log(logname)





# ########### !!! if you don't close it, it will get overwritten
# when the next PYMAKR update is performed!!!!!!!!!!!
sd.closeSD('/' + conf.LOG_MOUNT)

