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
host = ''
espnowex.esp_tx(esp_con, 'get_time')
host, msg = espnowex.esp_rx(esp_con)

while not msg:
    retries += 1
    espnowex.esp_tx(esp_con, 'get_time')
    # print("Time Sensor: wait for time response")
    host, msg = espnowex.esp_rx(esp_con)
    print(f'found host: {host}')        
    print(f"Get Time: unable to get time ({retries})")
    time.sleep(3)

print(host)
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
# relay control, start in the off state
D8 = machine.Pin(15, machine.Pin.OUT)
D8.off()

# readings = dict() # in conf.py now
while True:
    # print(f"D7:{D7.value()} D8:{D8.value()}")

    # TODO this needs to be read from configuration
    readings = thermocouple.initReadings(conf.readings)
    # readings[1] = 0.0
    # readings[2] = 0.0
    # readings[3] = 0.0
    # readings[4] = 0.0
    # readings[5] = 0.0

    readings = thermocouple.read_thermocouples(readings)

  
    # for key in readings.keys():
    #     print(f"key: {key}, value: {readings[key]}")
    temperature_data = ','.join([str(value[2]) for value in readings.values()])
    # temperature_data = ','.join(map(str, readings.values()[1]))
    date_time = realtc.formattime(time.localtime())
    out = date_time + ',' + temperature_data
    print(out)
    espnowex.esp_tx(esp_con, out)

    # D8.on() # TESTING ONLY!!!!!!!!
    # TURN HEATER ON OR OFF
    # logic shouuld be on/off based on external reference
    # with check for any temperature above a maxium threshold for safety reasons

    diff = readings['HEATER'][2] - readings['CONTROL'][2]
    print(f"CHECK TEMP DIFFERENCE - cont:{readings['CONTROL'][2]}, heat:{readings['HEATER'][2]}, DIFFERENCE: {diff}")
    # print(f"temperature difference between heated and control leaf: {diff}")
    if diff <= 4.75:
        print("diff <= 4.5, D8 is on")
        D8.on()
    elif diff > 4.75 or diff == 'nan':
        print("diff >= 4.75 D8 is off")
        D8.off()
        # time.sleep(1.5)

    time.sleep(2)





# ########### !!! if you don't close it, it will get overwritten
# when the next PYMAKR update is performed!!!!!!!!!!!
# sd.closeSD(conf.LOG_MOUNT)

