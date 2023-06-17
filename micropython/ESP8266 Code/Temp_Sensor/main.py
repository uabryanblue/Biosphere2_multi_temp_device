import machine
import time

# import logger
import conf
import realtc
# import sd
import thermocouple
import espnowex

print("START TEMPERATURE SENSOR")

# con = espnowex.init_esp_connection()
sta, ap = espnowex.wifi_reset()
esp_con = espnowex.init_esp_connection(sta)


# convert hex into readable mac address
RAW_MAC = espnowex.get_mac(sta)
MY_MAC = ':'.join(['{:02x}'.format(b) for b in RAW_MAC])
# print(f"My MAC:: {MY_MAC}")
print(f"My MAC addres:: {MY_MAC} raw MAC:: {RAW_MAC}")

# set the time from the logger
retries = 0
while not espnowex.esp_tx(esp_con, 'get_time'):
    retries += 1
    print(f"Temp Sensor: unable to get time ({retries}), sleeping")
    time.sleep(3)

print("Time Sensor: wait for time response")
host, msg = espnowex.esp_rx(esp_con)
str_host = ':'.join(['{:02x}'.format(b) for b in host])
# assumption data is utf-8, if not, it may fail
str_msg = msg.decode('utf-8')
print("------------------------")
print(f"received a respons from {host} {str_host} of: {msg}") 
et = eval(msg)
print("--------------------")
print(f"et: {et}")
print("--------------------")

rtc = machine.RTC()
rtc.datetime(et)
print(f"Temp Sensor: the new time is: {realtc.formattime(time.localtime())}")  

# if retries == max_retries:
#     print("failed to set time!!!")
# else:
#     # get and set the time
#     print("get and set the date/time")
#     host, msg = espnowex.esp_rx(esp_con)
#     print(f"received a respons of: {msg}")
    
# setup pins for relays
# D7 = machine.Pin(13, machine.Pin.OUT)
# D7.on()
# sleep(2)
D8 = machine.Pin(15, machine.Pin.OUT)
D8.off()

readings = dict()
while True:
    # print(f"D7:{D7.value()} D8:{D8.value()}")

    # TODO this needs to be read from configuration

    readings[1] = 0.0
    readings[2] = 0.0
    readings[3] = 0.0
    readings[4] = 0.0
    readings[5] = 0.0

    readings = thermocouple.read_thermocouples(readings)

  
    # for key in readings.keys():
    #     print(f"key: {key}, value: {readings[key]}")
    temperature_data = ','.join(map(str, readings.values()))
    date_time = realtc.formattime(time.localtime())
    out = date_time + ',' + temperature_data
    print(out)
    espnowex.esp_tx(esp_con, out)

    # TURN HEATER ON OR OFF
    diff = readings[2] - readings[5]
    print(f"temperature difference between heated and control leaf: {diff}")
    if diff <= 4.75:
        print("diff <= 4.5, D8 is on")
        D8.on()
    elif diff > 4.75:
        print("diff >= 4.75 D8 is off")
        D8.off()

    time.sleep(1)





# ########### !!! if you don't close it, it will get overwritten
# when the next PYMAKR update is performed!!!!!!!!!!!
# sd.closeSD(conf.LOG_MOUNT)
