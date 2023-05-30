import machine
from time import sleep

# import logger
import conf
import realtc
import sd
import thermocouple
import lcd

print("START")

print("good to go")


# sleep(0.1)
log = conf.LOG_MOUNT + "/" + conf.LOG_FILENAME

# TODO this needs to be read from configuration
readings = dict()
readings[16] = 0.0
readings[0] = 0.0

for i in range(20):
    readings = thermocouple.read_thermocouples(readings)
 
    with open(log, "a") as f:
        f.write(f"{i}\t{realtc.formattime(time.localtime())}")
        for key in readings.keys():
            print(f"key: {key}, value: {readings[key]}")
            f.write(f"\t{readings[key]}")
        f.write("\n")

    sleep(1)

print("dump contents")
with open(log, "r") as f:
    for line in f:
        print(line.rstrip())
print("end of log")




# ########### !!! if you don't close it, it will get overwritten
# when the next PYMAKR update is performed!!!!!!!!!!!
sd.closeSD(conf.LOG_MOUNT)

